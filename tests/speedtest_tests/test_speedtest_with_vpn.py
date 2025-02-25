import csv
import random
from nordvpn import NordVPNAppAutomator
from ookla_speedtest import OoklaSpeedtest

def _get_random_country():
    """Get random country out of pre-defined list."""
    countries = ["United States", "Germany", "United Kingdom", "Canada", "France"]
    return random.choice(countries)

def _save_test_data(results, filename="vpn_speedtest_results.csv"):
    """
    Save the results list to a CSV file.

    :param results: Results gathered during testing.
    :param filename (optional): Name of the file to save results.
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Test Number', 'VPN Server', 'IP Before', 'IP After',
                         'Download Before (Mbps)', 'Download After (Mbps)',
                         'Upload Before (Mbps)', 'Upload After (Mbps)',
                         'Ping Before (ms)',  'Ping After (ms)',
                         'Server Info Before', 'Server Info After'])
        for result in results:
            for i, data in result.items():
                vpn_server, speedtest_data_before, speedtest_data_after = data
                writer.writerow([
                    i,
                    vpn_server,
                    speedtest_data_before.get('ip'), speedtest_data_after.get('ip'),
                    speedtest_data_before.get('download'), speedtest_data_after.get('download'),
                    speedtest_data_before.get('upload'), speedtest_data_after.get('upload'),
                    speedtest_data_before.get('ping'), speedtest_data_after.get('ping'),
                    speedtest_data_before.get('server'), speedtest_data_after.get('server')
                ])



def test_speedtest_with_vpn():
    vpn_automator = NordVPNAppAutomator()
    speed_tester = OoklaSpeedtest()
    results = []
    for i in range(20):
        print(f"Starting test number {i+1}...")
        if vpn_automator.is_vpn_connected():
            vpn_automator.disconnect_vpn()

        country = _get_random_country()

        print("Running speed test without VPN.")
        speedtest_data_before = speed_tester.run_speedtest()
        print("Speedtest data before VPN:", speedtest_data_before)

        vpn_automator.connect_to_country(country)
        vpn_server = vpn_automator.get_connected_server()

        print("Running speed test with VPN.")
        speedtest_data_after = speed_tester.run_speedtest()
        print("Speedtest data with VPN:", speedtest_data_after)

        results.append({
            f"Test #{i+1}": [vpn_server, speedtest_data_before, speedtest_data_after]
        })

        # Disconnect from VPN
        vpn_automator.disconnect_vpn()

    _save_test_data(results)
    vpn_automator.close_app()