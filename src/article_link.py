from bs4 import BeautifulSoup
import os
import requests

from src.utils import logger, random_string


TEST_IMG_TAG = "<img alt='רוני זהבי מנכ\"ל ומייסד היי-בוב ' class=\"hd-image calc-share-with-zoom\" " \
               "data-articleid=\"3880691\" data-title=\"חברת Hibob הישראלית גייסה 70 מיליון דולר\" data-url=\"" \
               "https://www.calcalist.co.il/internet/articles/0,7340,L-3880691,00.html\" " \
               "src=\"https://images1.calcalist.co.il/PicServer3/2020/12/10/1042961/R-s.jpg\" " \
               "title='רוני זהבי מנכ\"ל ומייסד היי-בוב '/>"

IMAGE_FOLDER = os.path.join('..', 'data')


class ArticleLink:
    def __init__(self, img_tag, out_dir=IMAGE_FOLDER):
        self._parse(img_tag)
        self._out_dir = out_dir
        if not os.path.exists(self._out_dir):
            os.mkdir(self._out_dir)

    def _parse(self, img_tag):
        self._title = img_tag.get('data-title')
        self._img_src = img_tag.get('src')
        self._url = img_tag.get('data-url')

    def download_image(self):
        if self._img_src is not None:
            filename = os.path.basename(self._img_src)
            file_path = os.path.join(self._out_dir, filename)
            if not os.path.exists(file_path):
                with open(file_path, "wb") as f:
                    f.write(requests.get(self._img_src).content)
                    logger.debug('Wrote file {}'.format(file_path))
            return file_path

    def __str__(self):
        return ' '.join([self._title, self._img_src, self._url])


if __name__ == '__main__':
    soup = BeautifulSoup(TEST_IMG_TAG, 'lxml')
    article = ArticleLink(soup.find('img'), IMAGE_FOLDER)
    print(article)
    article.download_image()
