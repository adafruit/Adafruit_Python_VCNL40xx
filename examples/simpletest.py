# Simple demo of of the VCNL4000 & VCNL4010 proximity sensor library.
# Will print the distance data every half second.
# Author: Tony DiCola
# License: Public Domain
import time

# Import the VCNL40xx module.
import Adafruit_VCNL40xx


# Create a VCNL4010 instance.
vcnl = Adafruit_VCNL40xx.VCNL4010()

# Or create a VCNL4000 instance.
#vcnl = Adafruit_VCNL40xx.VCNL4000()

# You can also override the I2C device address and/or bus with parameters:
#vcnl = Adafruit_VCNL40xx.VCNL4010(address=0x14, bus=2)

print('Printing proximity data (press Ctrl-C to quit)...')
while True:
    # Read proximity.
    proximity = vcnl.read_proximity()
    # Read the ambient light.
    ambient = vcnl.read_ambient()
    # Print out the results.
    print('Proximity={0}, Ambient light={1}'.format(proximity, ambient))
    # Wait half a second and repeat.
    time.sleep(0.5)
