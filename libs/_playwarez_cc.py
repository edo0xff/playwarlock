import requests

from bs4 import BeautifulSoup


class PlaywarezCC:


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


    def _getPvipVideoSource(self, iframe_src):
        video_id = iframe_src.split('/')[-1]

        headers = {
            'authority': 'pvip.nl',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://pvip.nl',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://pvip.nl/v/%s' % video_id,
            'accept-language': 'es-419,es;q=0.9,en;q=0.8,gl;q=0.7,la;q=0.6',
            'cookie': '_ym_uid=1608942855461123898; _ym_d=1608942855; __cfduid=d6ea87f3cd3af769d01ae3138eb5861571609291009',
        }

        data = {
          'r': '',
          'd': 'pvip.nl'
        }

        response = requests.post('https://pvip.nl/api/source/%s' % video_id, headers=headers, data=data)
        response = response.json()

        if not response['data'] == 'Video not found or has been removed':
            for file in response['data']:
                if file['label'] == '720p':
                    response = requests.get(file['file'], headers=headers, allow_redirects=False)
                    video_source = response.headers['Location']
                    return video_source

        else:
            print(response['data'])
            return False


    def _getVideoIframeSrc(self, url):
        with requests.Session() as request:
            response = request.get(url, headers=self.headers)

            soup = BeautifulSoup(response.text, "html.parser")
            iframe = soup.find('iframe')

        return iframe['src']


    def _searchResultFilter(self, results):
        filtered = []
        for result in results:
            link = result.find('a')
            if not '/episode/' in link['href']:
                thumbnail = link.find('img')['data-original']
                filtered.append((link['oldtitle'], link['href'], thumbnail))

        return filtered


    def isUrlForThisSite(self, url):
        return True if 'playwarez.cc' in url else False


    def search(self, query):
        results = []

        with requests.Session() as request:
            response = request.get("https://playwarez.cc/?s=%s" % "+".join(query.split(" ")), headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            results += self._searchResultFilter(soup.find_all('div', {'class': 'ml-item'}))

            pagination = soup.find('ul', {'class': 'pagination'})

            if not pagination:
                return

            pagination_links = pagination.find_all('a')
            pagination_links.pop(0)

            for pagination_link in pagination_links:
                response = request.get(pagination_link['href'], headers=self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                results += self._searchResultFilter(soup.find_all('div', {'class': 'ml-item'}))

        return results


    def getEpisodes(self, url):
        results = []

        with requests.Session() as request:
            response = request.get(url, headers=self.headers)

            soup = BeautifulSoup(response.text, "html.parser")
            seasons = soup.find_all('div', {'class': 'tvseason'})

            for season in seasons:
                season_title = season.find('strong').text.strip()
                links = season.find_all('a')
                for link in links:
                    try:
                        if 'episode' in link['href']:
                            title = "%s %s" % (season_title, link.text.strip())
                            results.append((title, link['href'].strip()))

                    except KeyError:
                        pass

        return results


    def getVideoSource(self, video_url):
        iframe_src = self._getVideoIframeSrc(video_url)

        if 'pvip.nl' in iframe_src:
            return self._getPvipVideoSource(iframe_src)
        else:
            print(' > Unsoported source origin %s' % iframe_src)
            return False
