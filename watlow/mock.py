"""Mock Watlow interface. Use for debugging systems."""

import asyncio
from random import random
from copy import deepcopy


class Gateway:
    """Mock interface to the Watlow Gateway used to communicate with ovens."""

    def __init__(self, *args, **kwargs):
        """Set random data."""
        super().__init__()
        self.state = {i: {'actual': 25, 'setpoint': 25} for i in range(1, 9)}

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
            elif temps['actual'] > temps['setpoint']:
                temps['actual'] -= 1

    async def get(self, zone):
        """Return a mock state with the same object structure."""
        await asyncio.sleep(random() * 0.25)
        self._perturb()
        return deepcopy(self.state.get(zone))

    async def set_setpoint(self, zone, setpoint):
        """Set a mock state."""
        await asyncio.sleep(random() * 0.25)
        self.state[zone]['setpoint'] = setpoint
