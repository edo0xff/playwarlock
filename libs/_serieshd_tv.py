import requests

from bs4 import BeautifulSoup


class SeriesHDTV:


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
        return True if 'serieshd.tv' in url else False


    def search(self, query):
        results = []

        with requests.Session() as request:
            response = request.get("https://www.serieshd.tv/buscar?s=%s" % "+".join(query.split(" ")), headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")

            items = soup.find_all('a', {'class': 'item-movie'})

            for result in items:
                thumbnail = "https://www.serieshd.tv%s" % result.find('img')['src']
                name = result.find('b', {'class': 'name'}).text
                results.append((name, result['href'], thumbnail))

        return results


    def getEpisodes(self, url):
        results = []

        with requests.Session() as request:
            response = request.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")

            seasons_links = soup.find_all('a', {'class': 'abrir_temporada'})

            for season_link in seasons_links:
                response = request.get(season_link['href'], headers=self.headers)
                soup = BeautifulSoup(response.text, "html.parser")

                episodes = soup.find('ul', {'class': 'list-episodios'})
                episodes_links = episodes.find_all('a')

                for episodes_link in episodes_links:
                    name = episodes_link.find('div', {'class': 'episodio'}).text
                    results.append((name, episodes_link['href']))

        return results

    def getVideoSource(self, video_url):
        headers = {
            'authority': 'www.serieshd.tv',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.serieshd.tv',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.serieshd.tv/serie/juego-de-tronos/temporada-1/episodio-1',
            'accept-language': 'es-419,es;q=0.9,en;q=0.8,gl;q=0.7,la;q=0.6',
            'cookie': '__cfduid=dd2930133572dffd3d0ba832425f402dd1609210619; XSRF-TOKEN=eyJpdiI6ImE3WVZqa1ZoM3NDYk9zazRXOVB2NHc9PSIsInZhbHVlIjoiUFp2Mjc1TG9GZm9ISkVmQjJDNkk1cFR5VHdFU1VrTzAxRXpoblliXC9wajZmdHpabTRTK0NKRCtiNXNGWUNXSTkxOVEzeGNiaEczY3NHcG4rd3JHaWhBPT0iLCJtYWMiOiJkZTg5OGMxMThmMTA0OWIzNWQxNTA1OWU1ZTI4N2QxMzgyYzM3MjUwZDhmOTI3ZWE0MTA4MmE3NjgyYjQ2ZTE1In0%3D; serieshdtv_session=eyJpdiI6ImxzNmJUR2N0bU1pTEJNWVZ3c3M4VUE9PSIsInZhbHVlIjoiOGVcLzE4eUtFdjYwY09oQjJwb2VkMGhaN2o1QnRPemQ3TEhZWG5lMVRDOWhhcFVBMkh6Y2NyVjhITnFzc1hnTW9YaUltQktnb1pnXC84enRuR3k3dFdUUT09IiwibWFjIjoiNjU1NzBjODIzNWIyZmJlM2M3MWI4ZGZhNzM4ZTgyOTU1MTIyZGI2Njg2Mjk5MjI2YjY0NjBiZTIyNWVkMzY2ZSJ9',
        }

        with requests.Session() as request:
            response = request.get(video_url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            servers_list = soup.find('ul', {'id': 'lista_online'})
            servers = servers_list.find_all('li', {'class', 'option'})

            for server in servers:
                if server['data-servidor'] == 'Vidoza':
                    data = {
                      'data': server['data-player'],
                      'tipo': 'videohost',
                      '_token': servers_list['data-token']
                    }

                    response = requests.post('https://www.serieshd.tv/entradas/procesar_player', headers=headers, data=data)
                    response = response.json()

                    response = request.get(response['data'], headers=self.headers)
                    soup = BeautifulSoup(response.text, "html.parser")

                    video = soup.find('video').find('source')
                    return video['src']

            return False
