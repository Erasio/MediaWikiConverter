import requests
import os.path
from os import path

from . import DataObjects
WikiPage = DataObjects.WikiPage

class MediaWikiDownloader:
    def __init__(self, cache = False, wikiURL = "http://www.ue4community.wiki/api.php"):
        self.continueTitle = ""
        self.currentPageTitles = []
        self.wikiURL = wikiURL
        self.doCache = cache
        if path.exists("WikiCache"):
            self.cacheExisting = True

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.currentPageTitles) == 0:
            self._downloadNextBatch_()

        nextTitle = self.currentPageTitles.pop(0)["title"]

        if self.cacheExisting:
            try:
                return self._readCache_(nextTitle)
            except:
                return self._downloadPage_(nextTitle)
        else:
            return self._downloadPage_(nextTitle)


    def _downloadNextBatch_(self):
        S = requests.Session()

        PARAMS = {
            "action": "query",
            "format": "json",
            "list": "allpages",
            "aplimit": 100,
            "apcontinue": self.continueTitle
        }

        R = S.get(url=self.wikiURL, params=PARAMS)
        DATA = R.json()

        self.currentPageTitles = DATA["query"]["allpages"]
        self.continueTitle = self.currentPageTitles[-1]["title"]

    def _downloadPage_(self, title):
        import requests

        S = requests.Session()

        PARAMS = {
            "action": "parse",
            "prop": "wikitext",
            "page": title,
            "format": "json"
        }

        R = S.get(url=self.wikiURL, params=PARAMS)
        DATA = R.json()

        try:
            page = WikiPage(title, DATA["parse"]["wikitext"]["*"])
        except:
            print(DATA)
            error("Download error!")

        if self.doCache:
            self._writeCache_(page)

        return page

    def _writeCache_(self, page):
        if not os.path.exists("WikiCache"):
            os.makedirs("WikiCache")
        
        f = open("WikiCache/" + page.title, "w", encoding='utf-8')
        f.write(page.content)
        f.close()

    def _readCache_(self, title):
        f = open("WikiCache/" + title, "r", encoding='utf-8')
        content = f.read()
        f.close()

        return WikiPage(title, content)
