from evdev import InputDevice, categorize, ecodes, list_devices
from select import select

dev = InputDevice('/dev/input/mouse1')

devices = map(InputDevice, list_devices())
for device in devices:
    print( '%-20s %-32s %s' % (device.fn, device.name, device.phys) )

while True:
    r, w, x = select([dev], [], [])
    for event in dev.read():
        print(categorize(event))
