import pytest


from tests.confest import full_data, not_full_data1, not_full_data2
from src.reports import spending_by_category


def test_spending_by_category(full_data, not_full_data1, not_full_data2):
    assert len(spending_by_category(full_data, "2", "12.09.2024")) == 2

    with pytest.raises(KeyError) as date_err:
        spending_by_category(not_full_data1, "2", "12.09.2024")

    assert str(date_err.value) == "KeyError('Дата платежа')"

    with pytest.raises(KeyError) as cat_err:
        spending_by_category(not_full_data2, "2", "12.09.2024")

    assert str(cat_err.value) == "KeyError('Категория')"
