from bs4 import BeautifulSoup
import os

from src.article_link import ArticleLink
from src.utils import logger, IMAGE_DIR

TEST_IMG_TAG = "<img alt='רוני זהבי מנכ\"ל ומייסד היי-בוב ' class=\"hd-image calc-share-with-zoom\" " \
               "data-articleid=\"3880691\" data-title=\"חברת Hibob הישראלית גייסה 70 מיליון דולר\" data-url=\"" \
               "https://www.calcalist.co.il/internet/articles/0,7340,L-3880691,00.html\" " \
               "src=\"https://images1.calcalist.co.il/PicServer3/2020/12/10/1042961/R-s.jpg\" " \
               "title='רוני זהבי מנכ\"ל ומייסד היי-בוב '/>"


def test_article_link():
    soup = BeautifulSoup(TEST_IMG_TAG, 'lxml')
    article = ArticleLink(soup.find('img'), IMAGE_DIR)
    assert article.img_out_path is None
    article.download_image()
    assert article.img_out_path is not None and os.path.exists(article.img_out_path)

