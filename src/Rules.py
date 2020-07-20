import re

class ConverterRule:
    def __init__(self):
        pass

    def apply(self):
        print("Error: ConverterRule without overwritten apply function!")
        pass

class ReplacementRule(ConverterRule):
    def __init__(self, oldString, newString):
        super().__init__()
        self.old = oldString
        self.new = newString
    
    def apply(self, wikiPage):
        wikiPage.content = wikiPage.content.replace(self.old, self.new)
        return wikiPage


class RegexRule(ConverterRule):
    def __init__(self, regex, replacement):
        super().__init__()
        self.old = regex
        self.new = replacement

    def apply(self, wikiPage):
        wikiPage.content = re.sub(self.old, self.new, wikiPage.content)
        return wikiPage

class CategoryRule(ConverterRule):
    def __init__(self):
        super().__init__()

    def apply(self, wikiPage):
        categories = []
        categories = re.findall("\[\[Category:(.*)\]\]", wikiPage.content)
        for category in categories:
            wikiPage.tags.append(category)

        wikiPage.content = re.sub("\[\[Category:(.*)\]\]", "", wikiPage.content)

        return wikiPage
