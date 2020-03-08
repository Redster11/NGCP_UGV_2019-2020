from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.devices import XBee64BitAddress
from digi.xbee.devices import serial
import json

keep_going = True

device = XBeeDevice("COM4", 9600)
device.open()
remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A200419475BB"))

#gcsID = 100
#target sugvID = 200
data_set = {"type": 'movement', "id": 1, "sid" : 100, "tid": 200, "time" : 500}

json_dump = json.dumps(data_set)

device.send_data(remote_device, json_dump)

print("Message sent")

try:
    device.flush_queues()

    print("Waiting for response...")

    keepRunning = True

    while keepRunning:
        xbee_message = device.read_data()
        if xbee_message is not None:
            json_object = json.loads(xbee_message.data.decode())
            print(json_object["type"])
            keepRunning = False

finally:
        if device is not None and device.is_open():
            device.close()

#type - aknowledge, connect, complete, update, control?
#sid - only be gcs until we look at bugv