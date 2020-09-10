# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import send_from_directory
from flask import request

def indexer_views(photomanager, socketio):
    bp = Blueprint('indexer', __name__, static_folder='static')

    # Path for our main Svelte page
    @bp.route("/get_photo")
    def get_pic():
        album = request.args.get('album')
        name = request.args.get('name')
        print("Sending photo {}/{}".format(album, name))
        return send_from_directory(album, name)

    return bp
