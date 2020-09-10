from .views import home_views
from os import walk, rename
from os.path import getmtime
import re


class Home:
    def __init__(self, app):
        self.bp = home_views(self, app.socketio)
        self.appmoduleslist = app.appmodules

    def get_name(self):
        return "home"

    def get_blueprint(self):
        return self.bp

    def updateIndex(self, path, file):
        oldfile = "{}/{}".format(path, file)
        newfile = "{}/{}.new".format(path, file)
        # Browse to get CSS and JS urls
        with open(newfile, 'wt') as foutidx:
            with open(oldfile, "rt") as finidx:
                for line in finidx.readlines():
                    res = re.search("link.*rel='stylesheet'.*href='([A-Za-z0-9./?-_=&]+)'", line)
                    if not res:
                        res = re.search("script.*src='([A-Za-z0-9./?-_=&]+)'", line)
                    if res:
                        targetfile = res.group(1).split('?')[0]
                        ts = getmtime("{}/{}".format(path, targetfile))
                        newline = line.replace(res.group(1), "{}?version={}".format(targetfile, ts))
                        foutidx.write(newline)
                        continue
                    else:
                        foutidx.write(line)
        rename(newfile, oldfile)
