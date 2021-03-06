from bs4 import BeautifulSoup
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, \
    ElementClickInterceptedException
import time

from src.article_link import ArticleLink
from src.get_links import CALCALIST_URL
from src.utils import logger, OUT_DIR

DRIVER_PATH = os.path.join('..', 'chrome_driver')
DRIVER_NAME = 'chromedriver.exe'
LOAD_PAUSE = 1.5

CALCALIST_LOAD_MORE_ITM = 'hlm-load-more'
OUT_PATH = os.path.join(OUT_DIR, 'out.csv')


def start_chrome_driver():
    opts = Options()
    opts.add_argument(' --headless')
    chrome_driver = os.path.join(DRIVER_PATH, DRIVER_NAME)
    driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)
    return driver


def driver_load_page(driver, url):
    driver.get(url)


def load_all_articles(driver):
    # TODO: fix not all data loaded
    ind = 0
    prev_height = 0
    while True:
        try:
            load_more = driver.find_element_by_class_name(CALCALIST_LOAD_MORE_ITM)
            height = driver.execute_script("return document.body.scrollHeight")
            logger.debug('Document height: {}'.format(height))
            if prev_height < height:
                driver.execute_script("arguments[0].click();", load_more)
                time.sleep(LOAD_PAUSE)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                ind += 1
                logger.info('Loaded new page no. {}'.format(ind))
            else:
                logger.info('Reached end of page')
                break
            prev_height = height
        except NoSuchElementException:
            logger.info('Load more element missing')
            break
        except ElementClickInterceptedException:
            logger.error('Click intercepted')
            break


def gather_articles(driver):
    soup_file = driver.page_source
    soup = BeautifulSoup(soup_file, 'lxml')
    articles = []
    for img_tag in soup.findAll('img'):
        url = img_tag.get(ArticleLink.URL_ATTR)
        if url is not None:
            article_link = ArticleLink(img_tag)
            article_link.download_image()
            articles.append(article_link)
    logger.info('Gathered {} articles'.format(len(articles)))
    return articles


def article_list_to_csv(out_csv, articles):
    csv_data = [article.to_dict() for article in articles]
    df = pd.DataFrame(csv_data)
    df.to_csv(out_csv, index=False, encoding='utf-8')


def main():
    chrome_driver = start_chrome_driver()
    driver_load_page(chrome_driver, CALCALIST_URL)
    load_all_articles(chrome_driver)
    articles = gather_articles(chrome_driver)
    article_list_to_csv(OUT_PATH, articles)
    chrome_driver.quit()


if __name__ == '__main__':
    main()
