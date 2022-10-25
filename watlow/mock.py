"""Mock Watlow interface. Use for debugging systems."""

import asyncio
from random import random
from copy import deepcopy
from unittest.mock import MagicMock

from watlow.driver import Gateway as realGateway


class AsyncClientMock(MagicMock):
    """Magic mock that works with async methods."""

    async def __call__(self, *args, **kwargs):
        """Convert regular mocks into into an async coroutine."""
        return super().__call__(*args, **kwargs)


class Gateway(realGateway):
    """Mock interface to the Watlow Gateway used to communicate with ovens."""

    def __init__(self, *args, max_temp=220, **kwargs):
        """Set random data."""
        self.setpoint_range = (10, max_temp)
        self.state = {i: {'actual': 25, 'setpoint': 25, 'output': 0} for i in range(1, 9)}
        self.client = AsyncClientMock()

    def __getattr__(self, attr):
        """Return False for any undefined method."""
        def handler(*args, **kwargs):
            return False
        return handler

    def _perturb(self):
        """Make the values dance a bit."""
        for temps in self.state.values():
            if temps['actual'] < temps['setpoint']:
                temps['actual'] += 1
                temps['output'] = min(temps['setpoint'] - temps['actual'], 100)
            elif temps['actual'] > temps['setpoint']:
                temps['actual'] -= 1
                temps['output'] = 0

    async def get(self, zone):
        """Return a mock state with the same object structure."""
        await asyncio.sleep(random() * 0.25)
        self._perturb()
        return deepcopy(self.state.get(zone))

    async def set_setpoint(self, zone, setpoint):
        """Set a mock state."""
        if not self.setpoint_range[0] <= setpoint <= self.setpoint_range[1]:
            raise ValueError(f"Setpoint ({setpoint}) is not in the valid range from"
                             f" {self.setpoint_range[0]} to {self.setpoint_range[1]}")
        await asyncio.sleep(random() * 0.25)
        self.state[zone]['setpoint'] = setpoint
