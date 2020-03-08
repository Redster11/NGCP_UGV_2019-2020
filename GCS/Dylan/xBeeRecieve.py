
from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.devices import XBee64BitAddress
import json

# TODO: Replace with the serial port where your local module is connected to.
PORT = "COM8"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600

 
def main():
    
    device = XBeeDevice(PORT, BAUD_RATE)
    remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A200418EA9DE"))
    try:
        device.open()

        device.flush_queues()

        print("Waiting for data...\n")

        while True:
            xbee_message = device.read_data()
            if xbee_message is not None:
                json_object = json.loads(xbee_message.data.decode())
                data = {"type": "Message Recieved " + json_object["type"], "sid": 200, "tid": 100}
                json_dump = json.dumps(data)
                print(json_object["tid"],json_object["sid"])
                if (json_object["tid"] == 200):
                    device.send_data(remote_device, json_dump)
                else:
                    print("Not working")
##                print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
##                                         xbee_message.data.decode()))

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
