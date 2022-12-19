import time
import requests


def random_ip_from_tmproxy(proxy_api_key):
    url1 = "https://tmproxy.com/api/proxy/get-current-proxy"
    url2 = "https://tmproxy.com/api/proxy/get-new-proxy"

    payload = {"api_key": proxy_api_key}

    while True:
        proxy = ''

        res = requests.post(url1, json=payload, timeout=2)

        if not res:
            time.sleep(10)
            continue

        if 'data' in res.json():
            if res.json()['data']['next_request'] == 0:
                requests.post(url2, json=payload, timeout=2)
                continue
            else:
                proxy = res.json()['data']['https']
                break
        else:
            time.sleep(15)
            requests.post(url2, json=payload, timeout=2)
            continue

    return proxy

def random_ip_from_tinsoftsv(proxy_api_key):
    url1 = "http://proxy.tinsoftsv.com/api/getProxy.php"
    url2 = "http://proxy.tinsoftsv.com/api/changeProxy.php"

    API_KEY = proxy_api_key

    params1 = {
        'key': API_KEY,
    }

    params2 = {
        'key': API_KEY,
        'location': 0
    }

    while True:
        proxy = ''

        res = requests.get(url1, params=params1)
        print(res.json())

        if not res:
            time.sleep(10)
            continue

        if 'description' in res.json() and res.json()['description'] == 'proxy not found!':
            time.sleep(15)
            requests.get(url2, params=params2)
            continue

        if 'proxy' in res.json():
            if res.json()['next_change'] == 0:
                requests.get(url2, params=params2)
                continue
            else:
                proxy = res.json()['proxy']
                break
        else:
            time.sleep(15)
            requests.get(url2, params=params2)
            continue

    return proxy

class Master:
    def __init__(self, proxy_api_key, proxy_source):
        self.proxy_api_key = proxy_api_key
        self.proxy_source = proxy_source
        # self.audio_crawler = YouTubeAudioDownloader()
        # self.processor = Processor()

    def random_ip(self):
        assert self.proxy_source in ['tinsoftsv', 'tmproxy']

        error_count = 0
        while True:
            try:
                if self.proxy_source == 'tmproxy':
                    self.ip = random_ip_from_tmproxy(proxy_api_key=self.proxy_api_key)
                elif self.proxy_source == 'tinsoftsv':
                    self.ip = random_ip_from_tinsoftsv(proxy_api_key=self.proxy_api_key)
                print(self.ip)
                return self.ip

            except Exception as e:
                print(e)
                if error_count == 10:
                    raise Exception('Random IP failed too much times')

                # error_logger.error('Random IP failed - proxy source: {}'.format(self.proxy_source),
                                #    exc_info=True)
                time.sleep(20)
                error_count += 1

# master = Master("bedf715e1b6830a6dc61ac805aafcee0","tinsoftsv")
# master.random_ip()

master = Master("bedf715e1b6830a6dc61ac805aafcee0","tmproxy")
master.random_ip()

# print(random_ip_from_tmproxy("a51ab19517f486f078dcd538dc3a9d55"))