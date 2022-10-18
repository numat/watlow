# watlow
Python driver and command-line tool for [Watlow EZ-Zone temperature controllers](https://www.watlow.com/en/products/controllers/temperature-and-process-controllers/ez-zone-pm-controller).

<p align="center">
  <img src="https://www.watlow.com/-/media/images/products/new--controllers/integrated-multi-function/tp_pm_480.ashx" />
</p>

Installation
============

```
pip install watlow
```

Usage
=====

### Command Line

```
$ watlow /dev/ttyUSB0
```

This returns a simple data structure.

```
{
  "actual": 21.66,
  "setpoint": 20.0,
  "output": 52.1
}
```

You can additionally use the `--set-setpoint` option to set a temperature setpoint.

If interacting with a Watlow RUI Gateway, the zone to get or set should be passed as a flag
```
$ watlow -z 1 192.168.1.101
```

See `watlow --help` for more.

### Python

#### Single Controller

For a single temperature controller, the python interface is basic synchronous serial communication.

```python
import watlow

tc = watlow.TemperatureController('/dev/ttyUSB0')

tc.set(30)
print(tc.get())
```

The driver is designed to be fault tolerant over long polling, and should
appropriately reconnect if its `IOError`s are managed. Here's an implementation
with standard long-poll exception handling. This should run until interrupted and
then exit cleanly.

```python
from time import sleep
import watlow

tc = watlow.TemperatureController('/dev/ttyUSB0')
try:
    while True:
        try:
            print(tc.get())
        except IOError:
            print('disconnected')
        sleep(1)
except KeyboardInterrupt:
    pass
finally:
    tc.close()
```

#### Gateway

The Gateway driver uses Python ≥3.7's async/await syntax to asynchronously communicate with
the gateway over ModBus-TCP.

```python
import asyncio
import watlow

async def run():
    async with watlow.Gateway('192.168.1.101') as gateway:
        print(await gateway.get(1))

asyncio.run(run())
```

Additionally, there is a mock for the Gateway driver available at `watlow.mock.Gateway` for testing.
