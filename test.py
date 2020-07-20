from src.DataObjects import WikiPage
from src.Converter import Converter
from src.TestData import Tests
from src.Downloader import MediaWikiDownloader
from src import Rules

class NewWikiConverter(Converter):
    def __init__(self, verbose = False):
        super().__init__("markdown_github", verbose = verbose)
        self.addPreRule(Rules.CategoryRule())
        self.addPreRule(Rules.ReplacementRule("==", "==="))
        
        # Special label mediawiki templates
        self.addPreRule(Rules.ReplacementRule("{{draft}}", "@@@draft@@@"))

        # Remove XML / HTML tags
        #self.addPreRule(Rules.RegexRule("(<)(.*)(>)", ""))

        # Translate mediawiki templates to new wiki syntax
        self.addPostRule(Rules.ReplacementRule("@@\\@draft@@@", "@alert info \n## Draft\nThis article is a preliminary version and is subject to change.\n@endalert"))


def writeToFile(filename, content):
    if content is None:
        return
    f = open(filename, "w")
    f.write(content)
    f.close()

# Converter class pre and post processing all data based on the defined rules
c = NewWikiConverter(verbose = False)
# Iterator downloading and if so desired caching all wiki pages from the mediawiki
mwd = MediaWikiDownloader(cache = True)

for page in mwd:
    # Convert while applying all modifiers
    convertedPage = c.translate(page)

    print("Successfully converted: " + convertedPage.title)
    print("Categories: ")
    for cat in convertedPage.tags:
        print("\t" + cat)
    print()


# Simpler test environment with access to data between steps for debugging
#output = WikiPage("SimpleTest", Tests.shortTest)
#output = WikiPage("ComplexTest", Tests.complexTest)
#c._preProcess_(output)
#c._process_(output)
#c._postProcess_(output)

#writeToFile("testOutput.md", output.content)
