from src.title_analyzer import FundingTitle


FUNDING_TEXT = 'חברת Hibob הישראלית גייסה 70 מיליון דולר'
FUNDING_COMPANY = 'Hibob'
FUNDING_MONEY = 70000000

NON_FUNDING_TEXT = 'יצחק תשובה ירד בהנפקה לאחזקה של 50.01% בקבוצת דלק'


def test_funding_title():
    ft = FundingTitle(FUNDING_TEXT)
    assert ft.is_funding
    assert ft.company == FUNDING_COMPANY
    assert ft.money == FUNDING_MONEY


def test_non_funding_title():
    ft = FundingTitle(NON_FUNDING_TEXT)
    assert not ft.is_funding
    assert ft.company is None
    assert ft.money == 0

