# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

import time
import re


class TestFtu(GaiaTestCase):

    _activation_section_locator = ('id', 'activation')
    _main_title_locator = ('id', 'main_title')

    _next_button_locator = ('id', 'forward')

    # Step Languages section
    _section_languages_locator = ('id', 'languages')
    _listed_languages_locator = ('css selector', "#languages ul li input[name='language.current']")

    # Step Cell data section
    _section_cell_data_locator = ('id', 'data_3g')
    _enable_data_checkbox_locator = ('id', 'data-connection-switch')

    # Step Wifi
    _section_wifi_locator = ('id', 'wifi')
    _found_wifi_networks_locator = ('css selector', 'ul#networks-list li')
    _network_state_locator = ('xpath', 'p[2]')
    _password_input_locator = ('id', 'wifi_password')
    _join_network_locator = ('id', 'wifi-join-button')

    # Step Date & Time
    _section_date_time_locator = ('id', 'date_and_time')
    _timezone_continent_locator = ('id', 'tz-region')
    _timezone_city_locator = ('id', 'tz-city')
    _time_zone_title_locator = ('id', 'time-zone-title')

    # Section Import contacts
    _section_import_contacts_locator = ('id', 'import_contacts')
    _import_from_sim_locator = ('id', 'sim-import-button')
    _sim_import_feedback_locator = ('css selector', '.ftu p')

    # Section About Your rights
    _section_ayr_locator = ('id', 'about-your-rights')

    # Section Welcome Browser
    _section_welcome_browser_locator = ('id', 'welcome_browser')
    _enable_statistic_checkbox_locator = ('id', 'share-performance')

    # Section Privacy Choices
    _section_browser_privacy_locator = ('id', 'browser_privacy')
    _email_field_locator = ('css selector', 'input[type="email"]')

    # Section Finish
    _section_finish_locator = ('id', 'finish-screen')
    _skip_tour_button_locator = ('id', 'skip-tutorial-button')
    _take_tour_button_locator = ('id', 'lets-go-button')

    # Section Tour
    _step1_header_locator = ('id', 'step1Header')
    _step2_header_locator = ('id', 'step2Header')
    _step3_header_locator = ('id', 'step3Header')
    _step4_header_locator = ('id', 'step4Header')
    _step5_header_locator = ('id', 'step5Header')
    _tour_next_button_locator = ('id', 'forwardTutorial')
    _tour_back_button_locator = ('id', 'backTutorial')

    # Section Tutorial Finish
    _section_tutorial_finish_locator = ('id', 'tutorialFinish')
    _lets_go_button_locator = ('id', 'tutorialFinished')

    # Pattern for import sim contacts message
    _pattern_contacts = re.compile("^No contacts detected on SIM to import$|^Imported one contact$|^Imported [0-9]+ contacts$")
    _pattern_contacts_0 = re.compile("^No contacts detected on SIM to import$")
    _pattern_contacts_1 = re.compile("^Imported one contact$")
    _pattern_contacts_N = re.compile("^Imported ([0-9]+) contacts$")

    def setUp(self):
        GaiaTestCase.setUp(self)

        # We need WiFi enabled but not connected to a network
        self.data_layer.enable_wifi()
        self.data_layer.forget_all_networks()

        # Cell data must be off so we can switch it on again
        self.data_layer.disable_cell_data()

        # launch the First Time User app
        self.app = self.apps.launch('FTU')

    def create_language_locator(self, language):
        return ('css selector', "#languages ul li input[name='language.current'][value='%s']" % language)

    def test_ftu_skip_tour(self):
        # https://moztrap.mozilla.org/manage/case/3876/
        # 3876, 3879

        self.wait_for_element_displayed(*self._section_languages_locator)

        # FTU is not properly localized yet so let's just check some are listed
        # TODO enhance this to include lang selection when FTU is localized
        listed_languages = self.marionette.find_elements(*self._listed_languages_locator)
        self.assertGreater(len(listed_languages), 0, "No languages listed on screen")
        # select en-US due to the condition of this test is only for en-US
        listed_enUS_language = self.marionette.find_element(*self.create_language_locator("en-US"))
        listed_enUS_language.click()

        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_cell_data_locator)

        # Click enable data
        self.marionette.find_element(*self._enable_data_checkbox_locator).click()

        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_wifi_locator)

        # Wait for some networks to be found
        self.wait_for_condition(lambda m: len(m.find_elements(*self._found_wifi_networks_locator)) > 0,
                                message="No networks listed on screen")

        # TODO This will only work on Mozilla Guest or unsecure network
        wifi_network = self.marionette.find_element('id', self.testvars['wifi']['ssid'])
        wifi_network.click()

        # This is in the event we are using a Wifi Network that requires a password
        # We cannot be sure of this thus need the logic
        if self.testvars['wifi'].get('keyManagement'):

            self.wait_for_element_displayed(*self._password_input_locator)
            password = self.marionette.find_element(*self._password_input_locator)
            password.send_keys(self.testvars['wifi'].get('psk') or self.testvars['wifi'].get('wep'))
            self.marionette.find_element(*self._join_network_locator).click()

        self.wait_for_condition(
            lambda m: wifi_network.find_element(*self._network_state_locator).text == "Connected")

        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_date_time_locator)

        # Set timezone
        continent_select = self.marionette.find_element(*self._timezone_continent_locator)
        # Click to activate the b2g select element
        continent_select.click()
        self._select("Asia")

        city_select = self.marionette.find_element(*self._timezone_city_locator)
        # Click to activate the b2g select element
        city_select.click()
        self._select("Almaty")

        self.assertEqual(self.marionette.find_element(*self._time_zone_title_locator).text,
                         "UTC+06:00 Asia/Almaty")

        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_import_contacts_locator)

        # Click import from SIM
        # You can do this as many times as you like without db conflict
        self.marionette.find_element(*self._import_from_sim_locator).click()

        # TODO What if Sim has two contacts?
        # pass thid condition when contacts are 0~N
        self.wait_for_condition(lambda m: self._pattern_contacts.match(m.find_element(*self._sim_import_feedback_locator).text) is not None,
                                message="Contact did not import from sim before timeout")
        # Find how many contacts are imported.
        import_sim_message = self.marionette.find_element(*self._sim_import_feedback_locator).text
        import_sim_count = None
        if self._pattern_contacts_0.match(import_sim_message) is not None:
            import_sim_count = 0
        elif self._pattern_contacts_1.match(import_sim_message) is not None:
            import_sim_count = 1
        elif self._pattern_contacts_N.match(import_sim_message) is not None:
            count = self._pattern_contacts_N.match(import_sim_message).group(1)
            import_sim_count = int(count)

        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_welcome_browser_locator)

        # Click the statistics box and check that it sets a setting
        # TODO assert via settings API that this is set. Currently it is not used
        self.marionette.find_element(*self._enable_statistic_checkbox_locator).click()

        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_browser_privacy_locator)

        # Enter a dummy email address and check it set inside the os
        # TODO assert that this is preserved in the system somewhere. Currently it is not used
        self.marionette.find_element(*self._email_field_locator).send_keys("testuser@mozilla.com")

        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_finish_locator)

        # Skip the tour
        self.marionette.find_element(*self._skip_tour_button_locator).click()

        # Switch back to top level now that FTU app is gone
        self.marionette.switch_to_frame()

        self.assertEqual(len(self.data_layer.all_contacts), import_sim_count)
        self.assertTrue(self.data_layer.get_setting("ril.data.enabled"), "Cell data was not enabled by FTU app")
        self.assertTrue(self.data_layer.is_wifi_connected(self.testvars['wifi']), "WiFi was not connected via FTU app")

    def tearDown(self):

        # TODO flush any settings set by the FTU app
        self.data_layer.disable_cell_data()

        self.data_layer.disable_wifi()

        GaiaTestCase.tearDown(self)

    def _select(self, match_string):
        # Cheeky Select wrapper until Marionette has its own
        # Due to the way B2G wraps the app's select box we match on text

        # Have to go back to top level to get the B2G select box wrapper
        self.marionette.switch_to_frame()

        options = self.marionette.find_elements('css selector', '#value-selector-container li')
        close_button = self.marionette.find_element('css selector', 'button.value-option-confirm')

        # Loop options until we find the match
        for li in options:
            if li.text == match_string:
                li.click()
                break

        close_button.click()

        # Now back to app
        self.marionette.switch_to_frame(self.app.frame)
