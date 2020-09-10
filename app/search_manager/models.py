from .views.search import search_views
from os import walk

class SearchManager:
    def __init__(self, app):
        self.bp = search_views(self, app.socketio)
        self.appmoduleslist = app.appmodules

    def get_name(self):
        return "search_manager"

    def get_blueprint(self):
        return self.bp

    def list_pics(self, querypath):
        picslist = []
        for (dirpath, dirnames, filenames) in walk(querypath):
            for file in filenames:
                picslist.append({"name": file, "album": querypath})
            break
        return picslist
