from flask import Flask, redirect, url_for, request, jsonify, render_template

from libs import downloader, sites

app = Flask(__name__,
            template_folder='templates',
            static_url_path='',
            static_folder='static')


@app.route("/api/v0.1/search")
def search():
    query = request.args.get('q')

    if not query:
        return jsonify({'message':'missing argument: q'})

    all_results = []

    for site in sites:
        results = site.search(query)
        all_results.append((type(site).__name__, results))

    return jsonify({'data': all_results})


@app.route("/api/v0.1/episodes")
def list_episodes():
    url = request.args.get('url')

    if not url:
        return jsonify({'message':'missing argument: url'})

    for site in sites:
        if site.isUrlForThisSite(url):
            return jsonify({'data': site.getEpisodes(url)})

    return jsonify({'message': 'unsupported site'})


@app.route("/api/v0.1/video_source")
def get_video_source():
    url = request.args.get('url')

    if not url:
        return jsonify({'message':'missing argument: url'})

    for site in sites:
        if site.isUrlForThisSite(url):
            return jsonify({'data': site.getVideoSource(url)})

    return jsonify({'message': 'unsupported site'})


@app.route("/api/v0.1")
def api_home():
    return jsonify({'message':'api v0.1'})


@app.route("/")
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
