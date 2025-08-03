import pytest

from tests.confest import full_data, not_full_data, empty_data
from src.services import search_description


def test_search_description(full_data, not_full_data, empty_data):
    assert len(search_description("1", full_data)) == 3
    assert len(search_description("1", not_full_data)) == 2
    with pytest.raises(KeyError) as empty_err:
        search_description("1", empty_data)

    assert str(empty_err.value) == "'empty'"
