# -*- coding: utf-8 -*-
import pytest
import fsa_bot.lib as lib


@pytest.mark.lib
@pytest.mark.parametrize('csv_string,out', [
    (
        'a,x,y b,x,z a,y,x b,y,z a,z,z b,z,z',
        [{'trigger': 'a', 'source': 'x', 'target': 'y'}, {'trigger': 'b', 'source': 'x', 'target': 'z'}, {'trigger': 'a', 'source': 'y', 'target': 'x'}, {'trigger': 'b', 'source': 'y', 'target': 'z'}, {'trigger': 'a', 'source': 'z', 'target': 'z'}, {'trigger': 'b', 'source': 'z', 'target': 'z'}]  # noqa: E501
    )
])
def test_csv_convert(csv_string, out):
    assert out == lib.csv_string_to_dicts(csv_string)
