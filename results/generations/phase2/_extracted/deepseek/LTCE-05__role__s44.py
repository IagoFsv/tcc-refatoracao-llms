from html.parser import HTMLParser


class HelpParser(HTMLParser):
    def __init__(self, text):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.text = text
        self.tags = ''
        self.chartags = ''
        self.show = False
        self.hdrlink = False
        self.level = 0
        self.pre = False
        self.hprefix = ''
        self.nested_dl = False
        self.simplelist = False
        self.toc = []
        self.header = ''
        self.prevtag = None

    def indent(self, amt=1):
        self.level += amt
        self.tags = '' if self.level == 0 else 'l' + str(self.level)

    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3']:
            assert self.level == 0
            if self.show:
                indent = ('         ' if tag == 'h3' else
                          '     ' if tag == 'h2' else
                          '')
                self.toc.append((indent + self.header, self.text.index('insert')))
            self.tags = ''
        elif tag in ['span', 'em']:
            self.chartags = ''
        elif tag == 'a':
            self.hdrlink = False
        elif tag == 'pre':
            self.pre = False
            self.tags = ''
        elif tag in ['ul', 'dd', 'ol']:
            self.indent(-1)
        self.prevtag = (False, tag)


class _TextWidget:
    def __init__(self):
        self.calls = 0

    def index(self, mark):
        self.calls += 1
        return f"{self.calls}.0"


def run(html, show=True, header="Intro", level=0):
    parser = HelpParser(_TextWidget())
    parser.show = show
    parser.header = header
    parser.level = level
    parser.tags = "start"
    parser.chartags = "em"
    parser.hdrlink = True
    parser.pre = True
    parser.feed(html)
    parser.close()
    return {
        "toc": parser.toc,
        "tags": parser.tags,
        "chartags": parser.chartags,
        "hdrlink": parser.hdrlink,
        "pre": parser.pre,
        "level": parser.level,
        "prevtag": parser.prevtag,
    }
