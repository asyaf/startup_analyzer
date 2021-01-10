import os
import pandas as pd

from src.scrape_dynamic_page import OUT_PATH
from src.title_analyzer import FundingTitle
from src.utils import OUT_DIR


TITLE_COL = 'title'
POST_ANALYSIS_OUT = os.path.join(OUT_DIR, 'analysis.csv')
ANALYSIS_COLS = ['title', 'company', 'money']


def extract_title_info(df):
    titles = df[TITLE_COL]
    title_data = []
    for title in titles:
        ft = FundingTitle(title)
        if ft.is_funding:
            title_data.append([title, ft.company, ft.money])
        else:
            title_data.append([title, None, 0])
    return pd.DataFrame(title_data, columns=ANALYSIS_COLS)


def load_data(csv):
    return pd.read_csv(csv)


def main():
    df = load_data(OUT_PATH)
    only_relevant = extract_title_info(df)
    only_relevant.to_csv(POST_ANALYSIS_OUT)


if __name__ == '__main__':
    main()