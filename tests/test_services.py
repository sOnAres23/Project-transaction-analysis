from src.services import filtering_by_search

import pandas as pd


def test_filtering_by_search():
    file_operation = pd.read_excel("../data/operations.xlsx")
    assert type(filtering_by_search("Связь")) == type(file_operation)
