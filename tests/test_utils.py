import pandas
import pytest

from src.utils import get_transactions_xlsx


def test_get_transactions_xlsx():
    assert get_transactions_xlsx("../data/operations.xlsx").iloc[0][0] == "31.12.2021 16:44:00"

    with pytest.raises(pandas.errors.EmptyDataError) as empty_err:
        get_transactions_xlsx("../data/empty.xlsx")

    assert str(empty_err.value) == "empty"

    with pytest.raises(FileNotFoundError, match="404"):
        get_transactions_xlsx("../data/not.xlsx")
