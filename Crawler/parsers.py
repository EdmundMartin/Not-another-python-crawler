from lxml import html as htmlparser


class fast_parser(object):

    def __init__(self,html):
        self.dom = htmlparser.fromstring(html)

    def get_titles(self):
        try:
            title = self.dom.find('.//title').text
            return title.strip(), len(title.strip())
        except:
            return 'N/A', 'N/A'

    def get_canonicals(self):
        try:
            canonicals = self.dom.xpath("//link[@rel='canonical']/@href")
            canonical = canonicals[0]
            return canonical, len(canonicals)
        except:
            return 'N/A', 'N/A'

    def get_metaDescription(self):
        try:
            meta_description = self.dom.xpath("//meta[@name='description']/@content")
            meta_description = meta_description[0]
            return meta_description.strip(), len(meta_description.strip())
        except:
            return 'N/A', 'N/A'

    def get_robots(self):
        try:
            robots = self.dom.xpath("//meta[@name='robots']/@content")
            robots = robots[0]
            return robots
        except:
            return 'N/A'