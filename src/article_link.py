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
    SRC_ATTR = 'src'
    TITLE_ATTR = 'data-title'
    URL_ATTR = 'data-url'

    def __init__(self, img_tag, out_dir=IMAGE_FOLDER):
        self._parse(img_tag)
        self._out_dir = out_dir
        if not os.path.exists(self._out_dir):
            os.mkdir(self._out_dir)
        self._img_out_path = None

    def _parse(self, img_tag):
        self._title = img_tag.get(ArticleLink.TITLE_ATTR)
        self._img_src = img_tag.get(ArticleLink.SRC_ATTR)
        self._url = img_tag.get(ArticleLink.URL_ATTR)

    def download_image(self):
        if self._img_src is not None:
            # avoid duplicates by adding dirname to img name
            filename = os.path.basename(self._img_src)
            dirname = os.path.basename(os.path.dirname(self._img_src))
            dst_filename = '{}_{}'.format(dirname, filename)
            file_path = os.path.abspath(os.path.join(self._out_dir, dst_filename))
            if not os.path.exists(file_path):
                with open(file_path, "wb") as f:
                    f.write(requests.get(self._img_src).content)
                    logger.debug('Wrote file {}'.format(file_path))
            self._img_out_path = file_path

    def to_dict(self):
        return {'title': self._title,
                'img_src': self._img_src,
                'url': self._url,
                'img_out_path': self._img_out_path}


if __name__ == '__main__':
    soup = BeautifulSoup(TEST_IMG_TAG, 'lxml')
    article = ArticleLink(soup.find('img'), IMAGE_FOLDER)
    print(article)
    article.download_image()
