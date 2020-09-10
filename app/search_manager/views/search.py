# -*- coding: utf-8 -*-
from flask import send_from_directory
from flask import Blueprint

from flask_socketio import send, emit


def search_views(searchmanager, socketio):
    bp = Blueprint('search', __name__, static_folder='static')

    @socketio.on('search')
    def search(json):
        print("Searching directory: {}".format(json["directory"]))
        resultslist = searchmanager.list_pics(json["directory"])
        jsonresults = {
            "size": len(resultslist),
            "results": resultslist
        }
        print("Sending message: {}".format(jsonresults))
        emit('search_results', jsonresults)

    @socketio.on('search_completion')
    def search(json):
        print('Current search query: {}'.format( json["search_query"] ))

    return bp
