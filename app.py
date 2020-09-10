# -*- coding: utf-8 -*-
from flask import Flask
from flask_socketio import SocketIO

from app.home.models import Home
from app.search_manager.models import SearchManager
from app.photo_manager.models import PhotoManager

"""
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
"""

class PhotoManagerApp():   # metaclass=Singleton
    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, async_mode='eventlet')
        self.appmodules = {}

        self.add_app_module(Home)
        self.add_app_module(SearchManager)
        self.add_app_module(PhotoManager)

#        self.app.register_blueprint(home(self.socketio))
#        self.app.register_blueprint(search(self.socketio))
#        self.app.register_blueprint(photo_indexer)

        self.app.config.from_object('config')   # Now we can access the configuration variables via app.config["VAR_NAME"].

        print( "DEBUG TRACE -------------")
        for rule in self.app.url_map.iter_rules():
            print("Rule: {}".format(rule))

        for name in self.appmodules.keys():
            print("Module added: {}".format(name))

    def add_app_module(self, appmodule):
        am = appmodule(self)
        self.app.register_blueprint(am.get_blueprint())
        self.appmodules[am.get_name()] = am

    def start(self):
        self.socketio.run(self.app, debug=True, host='0.0.0.0')
#       app.run(debug=True, host='0.0.0.0')

if __name__ == "__main__":
    pm = PhotoManagerApp()
    pm.start()
