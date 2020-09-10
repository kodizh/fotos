# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import send_from_directory

from flask_socketio import send, emit


def home_views(home, socketio):
    bp = Blueprint('home', __name__, static_folder='static')

    # Path for our main Svelte page
    @bp.route("/")
    def root():
        home.updateIndex(bp.static_folder, 'index.html')
        return send_from_directory(bp.static_folder, 'index.html')

    # Path for all the static files (compiled JS/CSS, etc.)
    @bp.route("/<path:path>")
    def path(path):
        return send_from_directory(bp.static_folder, path)

    @socketio.on('client_connected')
    def handle_client_connect_event(json):
        print('received json: {0}'.format(str(json)))

    @socketio.on('message')
    def handle_json_button(json):
        print("Received message {}".format(json))
        # it will forward the json to all clients.
        send(json, json=True)

    return bp
