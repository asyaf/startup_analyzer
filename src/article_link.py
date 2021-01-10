import os
import requests
import time

from src.utils import logger, IMAGE_DIR


class ArticleLink:
    SRC_ATTR = 'src'
    TITLE_ATTR = 'data-title'
    URL_ATTR = 'data-url'
    IMG_PREFIX = 'https://images1.calcalist.co.il/PicServer3/'

    REQUEST_SLEEP = 5
    REQUEST_TRIALS = 3

    def __init__(self, img_tag, out_dir=IMAGE_DIR):
        self._parse(img_tag)
        self._out_dir = out_dir
        if not os.path.exists(self._out_dir):
            os.mkdir(self._out_dir)
        self.img_out_path = None

    def _parse(self, img_tag):
        self.title = img_tag.get(ArticleLink.TITLE_ATTR)
        self._img_src = img_tag.get(ArticleLink.SRC_ATTR)
        self._url = img_tag.get(ArticleLink.URL_ATTR)

    def _get_image(self):
        trial = 0
        while trial < ArticleLink.REQUEST_TRIALS:
            try:
                data = requests.get(self._img_src)
                return data
            except requests.exceptions.ConnectionError:
                time.sleep(ArticleLink.REQUEST_SLEEP)
                trial += 1
                logger.debug('Num trials: {}'.format(trial))
        return None

    def _create_img_path(self):
        # avoid duplicates by converting url to path
        if self._img_src.startswith(ArticleLink.IMG_PREFIX):
            dst_filename = self._img_src[len(ArticleLink.IMG_PREFIX):]
        else:
            return None
        dst_filename = dst_filename.replace('/', '_')
        file_path = os.path.abspath(os.path.join(self._out_dir, dst_filename))
        return file_path

    def _is_error(self, file_path):
        if file_path is None:
            logger.debug('Invalid file path {}'.format(self._img_src))
            return True
        if os.path.exists(file_path):
            logger.debug('File {} exists'.format(file_path))
            self.img_out_path = file_path
            return True
        return False

    def download_image(self):
        if self._img_src is not None:
            file_path = self._create_img_path()
            if self._is_error(file_path):
                return
            with open(file_path, "wb") as f:
                data = self._get_image()
                if data is None:
                    logger.debug('Failed to get file {}'.format(file_path))
                    return
                f.write(data.content)
                logger.debug('Wrote file {}'.format(file_path))
            self.img_out_path = file_path

    def to_dict(self):
        return {'title': self.title,
                'img_src': self._img_src,
                'url': self._url,
                'img_out_path': self.img_out_path}



