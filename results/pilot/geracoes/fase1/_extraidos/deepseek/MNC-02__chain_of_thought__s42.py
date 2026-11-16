class EmbedField:
    def __init__(self, name, value, inline=True):
        self.name = str(name)
        self.value = str(value)
        self.inline = inline

class EmbedFooter:
    def __init__(self, text=None, icon_url=None):
        self.text = text
        self.icon_url = icon_url

class Embed:
    def __init__(self, title=None, color=None):
        self.title = title
        self.color = color
        self.thumbnail = None
        self.fields = []
        self.footer = None

    def set_thumbnail(self, url):
        self.thumbnail = url
        return self

    def add_field(self, name, value, inline=True):
        self.fields.append(EmbedField(name, value, inline))
        return self

    def set_footer(self, text=None, icon_url=None):
        self.footer = EmbedFooter(text, icon_url)
        return self
