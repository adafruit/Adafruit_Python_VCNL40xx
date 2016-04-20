# The MIT License (MIT)
#
# Copyright (c) 2016 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import time


# Common VCNL40xx constants:
VCNL40xx_ADDRESS          = 0x13
VCNL40xx_COMMAND          = 0x80
VCNL40xx_PRODUCTID        = 0x81
VCNL40xx_IRLED            = 0x83
VCNL40xx_AMBIENTPARAMETER = 0x84
VCNL40xx_AMBIENTDATA      = 0x85
VCNL40xx_PROXIMITYDATA    = 0x87
VCNL40xx_PROXIMITYADJUST  = 0x8A
VCNL40xx_3M125            = 0
VCNL40xx_1M5625           = 1
VCNL40xx_781K25           = 2
VCNL40xx_390K625          = 3
VCNL40xx_MEASUREAMBIENT   = 0x10
VCNL40xx_MEASUREPROXIMITY = 0x08
VCNL40xx_AMBIENTREADY     = 0x40
VCNL40xx_PROXIMITYREADY   = 0x20

# VCBL4000 constants:
VCNL4000_SIGNALFREQ       = 0x89

# VCNL4010 constants:
VCNL4010_PROXRATE         = 0x82
VCNL4010_INTCONTROL       = 0x89
VCNL4010_INTSTAT          = 0x8E
VCNL4010_MODTIMING        = 0x8F
VCNL4010_INT_PROX_READY   = 0x80
VCNL4010_INT_ALS_READY    = 0x40


class VCNL40xxBase(object):
    """Base class for VCNL40xx proximity sensors."""

    def __init__(self, address=VCNL40xx_ADDRESS, i2c=None, **kwargs):
        """Initialize the VCNL40xx sensor."""
        # Setup I2C interface for the device.
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(address, **kwargs)

    def _wait_response(self, ready, timeout_sec):
        """Wait for a response to be ready (the provided ready bits are set).
        If the specified timeout (in seconds) is exceeded and error will be
        thrown.
        """
        # Wait for the measurement to be ready (or a timeout elapses).
        start = time.time()
        while True:
            # Check if the timeout has elapsed.
            if (time.time() - start) >= timeout_sec:
                raise RuntimeError('Exceeded timeout waiting for VCNL40xx response, check your wiring.')
            # Check if result is ready and return it.
            result = self._device.readU8(VCNL40xx_COMMAND)
            if (result & ready) > 0:
                return
            # Otherwise delay for a bit and try reading again.
            time.sleep(0.001)

    def read_proximity(self, timeout_sec=1):
        """Read the sensor proximity and return it as an unsigned 16-bit value.
        The larger the value the closer an object is to the sensor.
        """
        # Ask for a proximity measurement and wait for the response.
        self._device.write8(VCNL40xx_COMMAND, VCNL40xx_MEASUREPROXIMITY)
        self._wait_response(VCNL40xx_PROXIMITYREADY, timeout_sec)
        # Return the proximity response.
        return self._device.readU16BE(VCNL40xx_PROXIMITYDATA)

    def read_ambient(self, timeout_sec=1):
        """Read the ambient light sensor and return it as an unsigned 16-bit value.
        """
        # Ask for an ambient measurement and wait for the response.
        self._device.write8(VCNL40xx_COMMAND, VCNL40xx_MEASUREAMBIENT)
        self._wait_response(VCNL40xx_AMBIENTREADY, timeout_sec)
        # Return the ambient response.
        return self._device.readU16BE(VCNL40xx_AMBIENTDATA)


class VCNL4000(VCNL40xxBase):
    """VCNL4000 proximity sensor."""

    def __init__(self, **kwargs):
        """Initialize the VCNL4000 sensor."""
        super(VCNL4000, self).__init__(**kwargs)
        # Write proximity adjustement register.
        self._device.write8(VCNL40xx_PROXIMITYADJUST, 0x81)


class VCNL4010(VCNL40xxBase):
    """VCNL4010 proximity sensor."""

    def __init__(self, **kwargs):
        """Initialize the VCNL4010 sensor."""
        super(VCNL4010, self).__init__(**kwargs)
        # Enable interrupt for proximity data ready.
        self._device.write8(VCNL4010_INTCONTROL, 0x08)

    def _clear_interrupt(self, intbit):
        """Clear the specified interrupt bit in the interrupt status register.
        """
        int_status = self._device.readU8(VCNL4010_INTSTAT);
        int_status &= ~intbit;
        self._device.write8(VCNL4010_INTSTAT, int_status);

    def read_proximity(self, timeout_sec=1):
        """Read the sensor proximity and return it as an unsigned 16-bit value.
        The larger the value the closer an object is to the sensor.
        """
        # Clear any interrupts.
        self._clear_interrupt(VCNL4010_INT_PROX_READY)
        # Call base class read_proximity and return result.
        return super(VCNL4010, self).read_proximity(timeout_sec)

    def read_ambient(self, timeout_sec=1):
        """Read the ambient light sensor and return it as an unsigned 16-bit value.
        """
        # Clear any interrupts.
        self._clear_interrupt(VCNL4010_INT_ALS_READY)
        # Call base class read_ambient and return result.
        return super(VCNL4010, self).read_ambient(timeout_sec)
