import time
import speedtest

class OoklaSpeedtest:
    def __init__(self):
        pass

    def run_speedtest(self, retries=3, delay=3):
        """
        Run OOKLA speedtest with the best available server and return test results.

        :param retries: Max number of times to retry connection in case of failure.
        :param delay: Time of delay between retries in case of connection failure.
        """
        attempt = 0
        while attempt < retries:
            try:
                self.st = speedtest.Speedtest(secure=True)
                self.st.get_best_server()
                download = self.st.download() / 1_000_000  # MBPS
                upload = self.st.upload() / 1_000_000  # MBPS
                ping = self.st.results.ping
                public_ip = self.st.results.client.get('ip')
                server_info = self.st.results.server
                return {
                    'ip': public_ip,
                    'download': round(download, 2),
                    'upload': round(upload, 2),
                    'ping': round(ping, 2),
                    'server': server_info
                }
            except speedtest.SpeedtestBestServerFailure:
                attempt += 1
                print(f"Attempt to connect to speedtest servers failed.")
                time.sleep(delay)
            except Exception as e:
                print(f"Got error during OOKLA speedtest: {e}")
                return {}

        # If all attempts failed then return empty result set
        return {}