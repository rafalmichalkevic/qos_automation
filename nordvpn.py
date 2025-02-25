import time

from pywinauto import Desktop
from pywinauto.application import Application
from pywinauto.keyboard import send_keys

class NordVPNAppAutomator:
    NORD_VPN_PATH = r"C:\Program Files\NordVPN\NordVPN.exe"
    def __init__(self):
        running_apps = Desktop(backend="uia").windows(title_re=".*NordVPN.*")
        # If NordVPN is already running then close it and reopen
        if running_apps:
            self.app = Application(backend="uia").connect(title_re=".*NordVPN.*")
            self.app.kill()

        self.app = Application(backend="uia").start(self.NORD_VPN_PATH)
        self.window = self.app.window(title_re=".*NordVPN.*")
        self.window.wait('enabled', timeout=30)
        # Wait for additional 3 seconds for app to be fully open
        time.sleep(3)

    def get_connected_server(self):
        """Retrieve the name of the connected VPN server."""
        try:
            server_info = self.window.child_window(auto_id="VpnTitleText", control_type="Text").window_text()
            return server_info
        except Exception as e:
            print(f"Error fetching VPN server name: {e}")
            return "Unknown"

    def _wait_until_vpn_is_connected(self):
        """Wait for VPN to be connected."""
        connection_status = ''
        while connection_status.upper() != "AUTO-CONNECTED":
            connection_status = self.window.child_window(auto_id="ConnectionStatusText", control_type="Text").window_text()
            time.sleep(0.5)

        # Additional 5 seconds to be sure that everything is connected :)
        time.sleep(5)

    def connect_to_country(self, country):
        """
        Automate connecting to a specific country.

        :param country: Country that we want to connect to
        """
        try:
            # Try focusing the search box before entering text
            search_box = self.window.child_window(auto_id="ServersListSearchInputField", control_type="Edit")
            search_box.set_focus()
            # Clear search bar before typing
            send_keys('^a{BACKSPACE}')
            search_box.type_keys(country, with_spaces=True)
            # Wait for results in search box
            time.sleep(2)

            country_result = self.window.child_window(title_re=f"{country}.*", control_type="Text", found_index=0)
            country_result.click_input()
            self._wait_until_vpn_is_connected()
        except Exception as e:
            print(f"Error while connecting to {country}: {e}")

    def is_vpn_connected(self):
        """Check if VPN is connected"""
        connected_server = self.get_connected_server()
        return connected_server != "Not Connected"

    def disconnect_vpn(self):
        """Automate disconnecting from VPN."""
        try:
            disconnect_button = self.window.child_window(auto_id="DashboardVpnDisconnect", control_type="Button")
            disconnect_button.click_input()
            confirmation_button = self.window.child_window(title="Pause auto-connect", control_type="Text")
            if confirmation_button.exists():
                confirmation_button.click_input()
            time.sleep(5)
        except Exception as e:
            print(f"Error while disconnecting: {e}")

    def close_app(self):
        """Close the NordVPN app."""
        self.app.kill()