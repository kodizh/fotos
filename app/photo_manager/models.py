from .views.photo_indexer import indexer_views

class PhotoManager:
    def __init__(self, app):
        self.bp = indexer_views(self, app.socketio)
        self.appmoduleslist = app.appmodules

    def get_name(self):
        return "photo_manager"

    def get_blueprint(self):
        return self.bp
