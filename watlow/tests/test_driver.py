"""Test the driver correctly parses a tags file and responds with correct data."""
from unittest import mock

import pytest

from watlow import command_line
from watlow.mock import Gateway


@pytest.fixture
def gateway_driver(address='fake ip', **kwargs):
    """Confirm the gateway driver correctly initializes."""
    return Gateway(address, **kwargs)


@mock.patch('watlow.Gateway', Gateway)
def test_driver_cli(capsys):
    """Confirm the commandline interface works with reading a zone."""
    command_line(['fakeip', '-z', '1'])
    captured = capsys.readouterr()
    assert 'actual' in captured.out
    assert 'setpoint' in captured.out
    assert 'output' in captured.out


@mock.patch('watlow.Gateway', Gateway)
def test_driver_cli_setpoint(capsys):
    """Confirm the commandline interface works with changing a setpoint."""
    command_line(['fakeip', '-z', '1', '-f', '26'])
    captured = capsys.readouterr()
    assert '"setpoint": 26' in captured.out
    assert '"actual": 26' in captured.out
    with pytest.raises(SystemExit):
        command_line(['fakeip', '-z', 'bogus'])


@pytest.mark.asyncio
async def test_roundtrip(gateway_driver):
    """Confirm various datatypes are read back correctly after being set."""
    expected = {'setpoint': 25.0, 'actual': 25, 'output': 0}
    assert await gateway_driver.get(zone=1) == expected
    await gateway_driver.set_setpoint(zone=1, setpoint=12.3)
    expected = {'setpoint': 12.3, 'actual': 24, 'output': 0}
    assert await gateway_driver.get(zone=1) == expected


@pytest.mark.asyncio
async def test_set_errors(gateway_driver):
    """Confirm the driver gives an error on invalid set_setpoint() calls."""
    with pytest.raises(ValueError, match='not in the valid range'):
        await gateway_driver.set_setpoint(zone=1, setpoint=9000)
