from src.reports import spending_result, spending_by_category
import pandas as pd


def test_spending_result(spending_result_fix):
    @spending_result()
    def test_dataframe():
        df = pd.DataFrame({'Yes': [50, 21], 'No': [131, 2]})
        return df

    assert type(test_dataframe().to_dict()) == type(spending_result_fix)


def test_spending_by_category(result_spending_by_category):
    file_test = pd.read_excel("../data/test_services.xlsx")
    assert spending_by_category(file_test, "Фастфуд").to_dict() == result_spending_by_category
