import pytest
import fsa_bot.lib as lib
import sys
import io


@pytest.mark.lib
def test_main(capsys):
    lib.main()
    captured = capsys.readouterr()

    assert captured.out == 'Hello, World!\n'
