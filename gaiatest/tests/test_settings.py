# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestSettings(GaiaTestCase):

    def test_set_cell_data(self):
        setting_name = 'ril.data.enabled'

        self.lockscreen.unlock()

        self.data_layer.toggle_cell_data('true')
        self.assertTrue(self.data_layer.get_setting(setting_name))

        self.data_layer.toggle_cell_data('false')
        self.assertFalse(self.data_layer.get_setting(setting_name)['result'])

    def test_set_cell_roaming(self):
        setting_name = 'ril.data.roaming_enabled'

        self.lockscreen.unlock()

        self.data_layer.toggle_cell_roaming('true')
        self.assertTrue(self.data_layer.get_setting(setting_name))

        self.data_layer.toggle_cell_roaming('false')
        self.assertFalse(self.data_layer.get_setting(setting_name)['result'])

    def test_set_wifi(self):
        setting_name = 'wifi.enabled'

        self.lockscreen.unlock()

        self.data_layer.enable_wifi()
        self.assertTrue(self.data_layer.get_setting(setting_name))

        self.data_layer.disable_wifi()
        self.assertFalse(self.data_layer.get_setting(setting_name)['result'])
