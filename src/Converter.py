import pypandoc
from . import Rules
from . import Downloader

class Converter:
    def __init__(self, targetFormat="markdown", verbose = False):
        self.preRules = []
        self.postRules = []
        self.targetFormat = targetFormat
        self.verbose = verbose

    def addPreRule(self, newRule):
        if not isinstance(newRule, Rules.ConverterRule):
            raise TypeError("Trying to add a rule that's not of type 'ConverterRule'")

        self.preRules.append(newRule)

    def addPostRule(self, newRule):
        if not isinstance(newRule, Rules.ConverterRule):
            raise TypeError("Trying to add a rule that's not of type 'ConverterRule'")

        self.postRules.append(newRule)


    def _preProcess_(self, wikiPage):
        if len(self.preRules) == 0:
            return content

        if self.verbose:
            self._debugPrint_("{} PreProcess Rules found".format(len(self.preRules)))
            self._debugPrint_("PreProcess 0%", end = "\r")

        for ruleIndex in range(len(self.preRules)):
            wikiPage = self.preRules[ruleIndex].apply(wikiPage)
            
            if self.verbose:
                self._debugPrint_("PreProcess {}%".format(ruleIndex / len(self.preRules)), end = "\r")

        self._debugPrint_("PreProcess Done                    \n")

        return wikiPage
        

    def _process_(self, wikiPage):
        self._debugPrint_("Pandoc conversion\n")
        wikiPage.content = pypandoc.convert_text(wikiPage.content, self.targetFormat, format="mediawiki", extra_args=["--wrap=none"])
        return wikiPage

    def _postProcess_(self, wikiPage):
        if len(self.postRules) == 0:
            return wikiPage

        self._debugPrint_("{} PostProcess Rules found".format(len(self.postRules)))
        self._debugPrint_("PostProcess 0%", end = "\r")
        for ruleIndex in range(len(self.postRules)):
            wikiPage = self.postRules[ruleIndex].apply(wikiPage)
            self._debugPrint_("PostProcess {}%".format(ruleIndex / len(self.postRules)), end = "\r")

        self._debugPrint_("PostProcess Done                    \n")

        return wikiPage
        
    def _debugPrint_(self, msg, end="\n"):
        if self.verbose:
            print(msg, end=end)

    def translate(self, wikiPage):
        wikiPage = self._preProcess_(wikiPage)
        wikiPage = self._process_(wikiPage)
        return self._postProcess_(wikiPage)
