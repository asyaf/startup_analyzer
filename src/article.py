import lxml.html
from urllib import request

TEST_ARTICLE = 'https://www.geektime.co.il/breezometer-air-quality-data-becomes-a-part-of-apples-weather-app-in-ios-14-3/'


class Article:
    def __init__(self, url):
        self.url = url

    def parse(self):
        title = Article.get_title()

    def get_title(self):
        t = lxml.html.parse(request.urlopen(self.url))
        return t.find(".//title").text


if __name__ == '__main__':
    article = Article(TEST_ARTICLE)
    title = article.get_title()
    print(title)
