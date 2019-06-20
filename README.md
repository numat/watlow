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
  "setpoint": 20.0
}
```

You can additionally use the `--set-setpoint` option to set a temperature setpoint.
See `watlow --help` for more.

### Python

The python interface is basic synchronous serial communication.

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
