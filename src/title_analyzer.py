import chardet
from contextlib import redirect_stdout
import re

from src.utils import logger

from YAPWrapper.yap_api import YapApi


YAP_IP = '127.0.0.1:8000'
YAP_PART = 'dependency_part'


class YAPServerError(Exception):
    pass


def analyze_text(text):
    logger.info('Analyzing {}'.format(text))
    yap = YapApi()
    try:
        with redirect_stdout(None):
            tokenized_text, segmented_text, lemmas, dep_tree, md_lattice, ma_lattice = yap.run(text, YAP_IP)
    except TypeError:
        logger.error('YAP server not working. Check if there is at least 6GB of RAM available')
        raise YAPServerError
    return segmented_text


class FundingTitle:
    FUNDING_MONEY = {'מיליון דולר': 10 ** 6, 'מיליארד דולר': 10 ** 9}
    FUNDING_WORDS = ['גייס', 'גיוס']

    def __init__(self, text):
        self._title = text
        self.is_funding = FundingTitle._check_if_funding(self._title)
        if self.is_funding:
            self.company, self.money = FundingTitle._get_funding_data(self._title)
        else:
            logger.info('Not funding')
            self.company = None
            self.money = 0

    @staticmethod
    def _get_funding_data(text):
        try:
            segmented = analyze_text(text)
            company = FundingTitle._get_company(segmented)
        except YAPServerError:
            logger.error('Server error. Running simple analysis')
            company = FundingTitle._get_company(text)

        money = FundingTitle._get_money(text)
        logger.info('Company: {}, Money amount: {}'.format(company, money))
        return company, money

    @staticmethod
    def _get_company(txt):
        splitted = txt.split()
        for word in splitted:
            is_num = word.replace('.', '', 1).isdigit()
            if is_num:
                continue
            lang = chardet.detect(word.encode())
            if lang['encoding'] == 'ascii':
                return word
        return None

    @staticmethod
    def _get_money_amount(txt):
        expr = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
        if re.search(expr, txt) is not None:
            # take first number
            matches = re.findall(expr, txt)
            amount = matches[0]
            if '.' in amount:
                return float(amount)
            else:
                return int(amount)
        return 0

    @staticmethod
    def _get_money(txt):
        amount = FundingTitle._get_money_amount(txt)
        if amount == 0:
            return 0
        for heb, value in FundingTitle.FUNDING_MONEY.items():
            funding_hebrew = '{} {}'.format(amount, heb)
            if funding_hebrew in txt:
                return amount * value
        return 0

    @staticmethod
    def _check_if_funding(text):
        for word in FundingTitle.FUNDING_WORDS:
            if word in text:
                return True
        return False

