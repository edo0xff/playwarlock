
# PlayWarlock

Script para descargar series y películas fácil, rápido, gratis y sin anuncios.

## Instalación

Requiere python > 3.x

### Clonar repositorio

	git clone https://github.com/edo0xff/playwarlock.git
	cd playwarlock

### Instalar dependencias

	python3 -m pip install -l requirements.txt

## Modo de uso

### Busqueda

	python3 cli.py --search "juego de tronos"

o

	python3 cli.py -s "hombres de negro"

### Descargar

#### Película

	python3 cli.py --download https://playwarez.cc/hombres-de-negro-3-2012/ --output "Hombres de negro 3" --output-dir /home/user/Videos

#### Serie completa

Paso 1. Obtener el listado de capítulos

	mkdir /home/user/Videos/GoT
	python3 cli.py --list-episodes https://www.serieshd.tv/serie/juego-de-tronos > /home/user/Videos/GoT/got-episodes.txt

Nota: Puedes quitar del archivo txt los episodios que no desees descargar.

Paso 2. Descarga

	python3 cli.py --batch-download /home/user/Videos/GoT/got-episodes.txt --output-dir /home/user/Videos/GoT

### API

API para en un futuro implementar la herramienta como una interfaz web.

	python3 api_server.py

Acceder desde el navegador a la dirección *http://localhost/api/v0.1*

Rutas soportadas por la API:

- **/api/v0.1/** *Muestra info de la API*
- **/api/v0.1/search** *Realizar busqueda de series y peliculas*
	- Parámetros
		- q *Argumento de busqueda*
	- Ejemplo
		- /api/v0.1/search?q=juego+de+tronos
- **/api/v0.1/episodes** *Lista episodios de una serie*
	- Parámetros
		- url *URL de la serie*
	- Ejemplo
		- /api/v0.1/episodes?url=https://playwarez.cc/series/juego-de-tronos-gratis-a/
- **/api/v0.1/video_source** *Devuelve la dirección el archivo de origen (mp4) del episodio/película*
	- Parámetros
		- url *URL del episodio o película*
	- Ejemplo
		- /api/v0.1/video_source?url=https://playwarez.cc/episode/juego-de-tronos-season-4-episode-8

## Webs soportadas

- playwarez.cc
- serieshd.tv

## ToDo

- Hacer que funcione con más páginas
- crear un cliente web para la API

## Contributors

- [edo0xff]([https://github.com/edo0xff](https://github.com/edo0xff))
