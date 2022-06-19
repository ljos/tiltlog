import asyncio
import binascii

from datetime import datetime

import bleak

from .config import settings
from .google import Store

UUID_DEVICE = {color: uuid for color, uuid in settings.devices.items()}


def f_to_c(value):
    return (value - 32) * (5/9)

def tilt_data(data):

    data = data['manufacturer_data']
    data = data[76]

    uuid = binascii.hexlify(data[2:18]).decode('utf-8')
    color = UUID_DEVICE[uuid]

    celsius = f_to_c(data[18] * 256 + data[19])
    specific_gravity = (data[20] * 256 + data[21]) / 1000

    return str(datetime.now()), color, celsius, specific_gravity


async def main():
    devices = await bleak.BleakScanner.discover(timeout=5.0)

    values = []
    for d in devices:
        try:
            data = tilt_data(d.metadata)
            values.append(data)
        except:
            pass

    return values


data = asyncio.run(main())

for ts, color, c, sg in data:
    print(f"{ts}\t{color}\t{c:.1f}°C\t{sg} SG")


store = Store(spreadsheet_id=settings.SPREADSHEET_ID)

store.append(data)
