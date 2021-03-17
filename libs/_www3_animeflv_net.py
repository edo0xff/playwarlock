import re
import json

from . import base


class WWW3AnimeFlvNET(base.SiteBase):


    def __init__(self):
        super().__init__()
        self.hostname = "www3.animeflv.net"


    def search(self, query):
        results = []

        with self.requests.Session() as request:
            search_url = "https://www3.animeflv.net/browse?q=%s" % self._urlEncode(query)
            response = request.get(search_url, headers=self.headers)
            soup = self.soup(response.text, "html.parser")

            items = soup.find('ul', {'class': 'ListAnimes'}).find_all('li')

            for result in items:
                title = result.find('h3', {'class': 'Title'}).text
                url = "https://www3.animeflv.net%s" % result.find('a')['href']
                thumbnail = result.find('img')['src']

                results.append((title, url, thumbnail))

        return results


    def getEpisodes(self, url):
        results = []

        with self.requests.Session() as request:
            response = request.get(url, headers=self.headers)
            soup = self.soup(response.text, "html.parser")

            anime_info_regex = r'var anime_info = (.*)\;'
            episodes_regex = r'var episodes = (.*)\;'

            anime_info = re.findall(anime_info_regex, response.text)
            episodes = re.findall(episodes_regex, response.text)

            anime_info = json.loads(anime_info[0])
            episodes = json.loads(episodes[0])

            for episode in episodes:
                title = "%s Episodio %s" % (anime_info[1], episode[0])
                url = "https://www3.animeflv.net/ver/%s-%s" % (anime_info[2], episode[0])

                results.append((title, url))

        results.reverse()
        return results


    def getVideoSource(self, url):
        with self.requests.Session() as request:
            response = request.get(url, headers=self.headers)

            videos_regex = r'var videos = (.*);'

            videos = re.findall(videos_regex, response.text)

            videos = json.loads(videos[0])

            for server in videos['SUB']:
                if server['server'] == 'gocdn':
                    code = server['code'].split('#')[1]
                    source_url = "https://streamium.xyz/gocdn.php?v=%s" % code

                    response = request.get(source_url, headers=self.headers)
                    response = response.json()

                    return response['file']
