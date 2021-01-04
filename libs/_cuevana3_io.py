from . import base


class Cuevana3IO(base.SiteBase):


    def __init__(self):
        super().__init__()
        self.hostname = "cuevana3.io"


    def search(self, query):
        results = []

        with self.requests.Session() as request:
            response = request.get("https://cuevana3.io/?s=%s" % "+".join(query.split(" ")), headers=self.headers)
            soup = self.soup(response.text, "html.parser")

            items = soup.find_all('li', {'class': 'TPostMv'})

            for item in items:
                title = item.find('div', {'class': 'Title'}).text
                url = item.find('a')['href']
                thumbnail = item.find('img')['data-src']

                results.append((title, url, thumbnail))

        return results


    def getEpisodes(self, url):
        results = []

        with self.requests.Session() as request:
            response = request.get(url, headers=self.headers)
            soup = self.soup(response.text, "html.parser")

            seasons = soup.find_all('ul', {'class': 'all-episodes'})

            for season in seasons:
                chapters = season.find_all('article')

                for chapter in chapters:
                    title = chapter.find('h2', {'class': 'Title'}).text
                    url = chapter.find('a')['href']

                    results.append((title, url))

        return results


    def getVideoSource(self, url):
        with self.requests.Session() as request:
            response = request.get(url, headers=self.headers)
            soup = self.soup(response.text, "html.parser")

            player = soup.find('div', {'class': ['TPlayerTb', 'Current']})
            iframe_src = "https:%s" % player.find('iframe')['data-src']

            response = request.get(iframe_src, headers=self.headers)
            soup = self.soup(response.text, "html.parser")

            redir = soup.find('form').find('input')['value']

            data = {
              'url': redir
            }

            response = request.post('https://api.cuevana3.io/ir/redirect_ddh.php', headers=self.headers, data=data, allow_redirects=False)
            video_id = response.headers['Location'].split("#")[1]

            response = request.get('https://damedamehoy.xyz/details.php?v=%s' % video_id, headers=self.headers)
            response = response.json()

            return response['file']
