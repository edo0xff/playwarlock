import requests

from bs4 import BeautifulSoup


class Cuevana3IO:


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


    def isUrlForThisSite(self, url):
        return True if 'cuevana3.io' in url else False


    def search(self, query):
        results = []

        with requests.Session() as request:
            response = request.get("https://cuevana3.io/?s=%s" % "+".join(query.split(" ")), headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")

            items = soup.find_all('li', {'class': 'TPostMv'})

            for item in items:
                title = item.find('div', {'class': 'Title'}).text
                url = item.find('a')['href']
                thumbnail = item.find('img')['data-src']

                results.append((title, url, thumbnail))

        return results


    def getEpisodes(self, url):
        results = []

        with requests.Session() as request:
            response = request.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")

            seasons = soup.find_all('ul', {'class': 'all-episodes'})

            for season in seasons:
                chapters = season.find_all('article')

                for chapter in chapters:
                    title = chapter.find('h2', {'class': 'Title'}).text
                    url = chapter.find('a')['href']

                    results.append((title, url))

        return results


    def getVideoSource(self, url):
        with requests.Session() as request:
            response = request.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")

            player = soup.find('div', {'class': ['TPlayerTb', 'Current']})
            iframe_src = "https:%s" % player.find('iframe')['data-src']

            response = requests.get(iframe_src, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")

            self.headers['Cookie'] = response.headers['Set-Cookie']

            redir = soup.find('form').find('input')['value']

            data = {
              'url': redir
            }

            response = requests.post('https://api.cuevana3.io/ir/redirect_ddh.php', headers=self.headers, data=data, allow_redirects=False)
            video_id = response.headers['Location'].split("#")[1]

            response = request.get('https://damedamehoy.xyz/details.php?v=%s' % video_id, headers=self.headers)
            response = response.json()

            return response['file']
