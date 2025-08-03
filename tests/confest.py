import pytest
from pandas import DataFrame


@pytest.fixture
def full_data():
    return DataFrame({"Описание": ["1", "1", "2", "3"],
                      "Категория": ["2", "2", "3", "1"],
                      "Дата платежа": ["12.09.2024", "12.08.2024", "12.07.2024", "10.06.2024"]})


@pytest.fixture
def not_full_data():
    return DataFrame({"Описание": ["1", "1", "2", "3"]})


@pytest.fixture
def not_full_data1():
    return DataFrame({"Категория": ["2", "2", "3", "1"]})


@pytest.fixture
def not_full_data2():
    return DataFrame({"Дата платежа": ["12.09.2024", "12.08.2024", "12.07.2024", "10.06.2024"]})


@pytest.fixture
def empty_data():
    return DataFrame({})
