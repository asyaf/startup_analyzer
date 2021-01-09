import ahocorasick
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urljoin
import requests

GEEKTIME_URL = 'https://www.geektime.co.il'
GEEKTIME_SUB_URL = 'category/startup/'
GEEKTIME_FILTERS = ['category', 'channel', '.php', 'author', 'contact']

CALCALIST_URL = 'https://www.calcalist.co.il/home/0,7340,L-3704-1822,00.html'


class Site:
    def __init__(self, url, sub_urls, filters):
        self.url = url
        self.sub_urls = sub_urls
        self.filters = filters

    def get_all_links(self):
        all_links = []
        if len(self.sub_urls) > 0:
            for sub_url in self.sub_urls:
                full_url = urljoin(self.url, sub_url)
                all_links.extend(self.get_links_from_url(full_url))
        else:
            all_links = self.get_links_from_url(self.url)
        return all_links

    def get_links_from_url(self, url):
        req = Request(url)
        html_page = urlopen(req)

        soup = BeautifulSoup(html_page, "lxml")
        print(soup)
        links = []
        # for link in soup.findAll('li'):
        #     # print(link)
        #     list_class = link.get('class')
        #     if list_class is None:
        #         print(link)
        #     # if self.is_valid_link(curr_link):
        #     #     links.append(curr_link)
        return links

    def is_valid_link(self, url_to_check):
        if url_to_check is None or self.url == url_to_check \
                or self.url not in url_to_check:
            return False
        if len(self.filters) > 0:
            automaton = ahocorasick.Automaton()
            for index, word in enumerate(self.filters):
                automaton.add_word(word, (index, word))
            automaton.make_automaton()
            items = list(automaton.iter(url_to_check))
            if len(items) > 0:
                return False
        return Site.is_url(url_to_check)

    @staticmethod
    def is_url(url):
        request = requests.get(url)
        return request.status_code == 200


if __name__ == '__main__':
    # geektime = Site(GEEKTIME_URL, [GEEKTIME_SUB_URL], GEEKTIME_FILTERS)
    # links = geektime.get_all_links()
    site = Site(CALCALIST_URL, [], [])
    links = site.get_all_links()
    for link in links:
        print(link)
