import requests

from bs4 import BeautifulSoup


class SiteBase:


    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        self.hostname = None
        self.requests = requests
        self.soup = BeautifulSoup


    def isUrlForThisSite(self, url):
        if not self.hostname:
            print("[%s] site_hostname error" % type(self).__name__)
            return False

        return True if self.hostname in url else False


    def search(self, query):
        print("[%s] search() should be implemented" % type(self).__name__)


    def getEpisodes(self, url):
        print("[%s] getEpisodes() should be implemented" % type(self).__name__)


    def getVideoSource(self, url):
        print("[%s] getVideoSource() should be implemented" % type(self).__name__)
