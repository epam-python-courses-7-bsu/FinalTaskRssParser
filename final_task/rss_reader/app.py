from flask import Flask, request, Response, send_from_directory
import os
import sys

from . import collect_news, version, get_cache, logg


app = Flask(__name__)


@app.route('/print/', methods=['GET', 'POST'])
def getNews():
    req = request.get_json()
    news = collect_news.collectNews(req['limit'], req['tojson'], req['tohtml'], req['topdf'], req['color'], req['url'])
    return sendResponse(req, news)


@app.route('/getcache/')
def getCacheNews():
    req = request.get_json()
    if(req['tohtml'] or req['topdf']):
        news = get_cache.createHtmlFromDB(req['limit'], req['tohtml'], req['topdf'], req['date'])
    else:
        news = get_cache.collectNewsFromDB(req['limit'], req['tojson'], req['color'], req['date'])
    return sendResponse(req, news)


def sendResponse(req, news):
    if(req['topdf']):
        try:
            return send_from_directory(req['topdf'], filename=news, as_attachment=True)
        except FileNotFoundError:
            abort(404)
    else:
        return Response(news)


@app.route('/version/', methods=['GET', 'POST'])
def getVersion():
    req = request.get_json()
    return version.VERSION


@app.route('/verbose/', methods=['GET', 'POST'])
def setLogging():
    logg.makeVerbose()


if __name__ == '__main__':
    app.run()
