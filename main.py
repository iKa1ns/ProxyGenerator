import random
from threading import Thread
import requests


class ProxyGen:
    """
    Class for generate and check proxy.
    """

    def __init__(self):
        self.d = {}

    @staticmethod
    def get_free_proxy_list() -> list:
        """
        Get and return list of proxy from GitHub

        :return: list of proxy
        """
        url = 'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt'
        r = requests.get(url)
        proxies = r.text.split('\n')
        return proxies

    def check_proxy_list(self, mass_of_proxies: list, timeout=5, count_of_proxy=None) -> None:
        """
        Method check list of proxies by request to server.
        Valid proxies add to dictionary named d -> {ip:count of valid checks}

        :param mass_of_proxies: list of proxies
        :param timeout: timeout of server
        :param count_of_proxy: quantity of proxies
        :return: None
        """
        url = 'https://www.babaip.com'
        while True:
            proxy = random.choice(mass_of_proxies)
            proxies = {"http": 'http://' + proxy, "https": 'http://' + proxy}
            if count_of_proxy:
                if len(self.d.keys()) > count_of_proxy:
                    break
            try:
                r = requests.get(url, timeout=timeout, proxies=proxies)
                if r.status_code == 200:
                    if proxy in self.d.keys():
                        self.d[proxy] += 1
                    else:
                        self.d[proxy] = 1
            except Exception as ex:
                print(ex)
                continue

    def generate_proxy(self, file_to_export=None, count_of_proxy=None, timeout=5, mass=None) -> None:
        """
        Method for generate valid proxies from GH or from your list

        :param file_to_export: file to export proxies. If None proxies print to stdout
        :param count_of_proxy: quantity of proxies what do you want to get
        :param timeout: timeout of server. (More timeout->more proxies->less quality)
        :param mass: list of your proxies to check
        :return: None
        """
        if not mass: mass = self.get_free_proxy_list()
        threads = [Thread(target=self.check_proxy_list, args=(mass, timeout, count_of_proxy)) for _ in range(250)]
        for thread in threads: thread.start()
        for thread in threads: thread.join()
        if file_to_export:
            with open(file_to_export, 'w') as f:
                [f.write(f'{i};{self.d[i]}\n') for i in self.d]
        else:
            print(self.d.keys())
