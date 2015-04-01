#from openxc.interface import BluetoothVehicleInterface

import argparse
import time
#import logging
from datetime import datetime, timedelta

from openxc.version import *
from common import device_options, configure_logging, select_device
from openxc.vehicle import Vehicle
from openxc.measurements import EventedMeasurement, Measurement, VehicleSpeed, Longitude, Latitude

def getVersion():
    return openxc.version.get_version()

def parse_options():
    parser = argparse.ArgumentParser(
            description="View a raw OpenXC data stream",
            parents=[device_options()])
    arguments = parser.parse_args()
    return arguments

class VehicleTest(object):
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.messages_received = []
        self.last_update_time = None
        self.vehicle.listen(VehicleSpeed, self.receive)
        self.vehicle.listen(Longitude, self.receive)
        self.vehicle.listen(Latitude, self.receive)

    def _update(self, measurement):
        if self.last_update_time is not None:
            time_since_update = timedelta.total_seconds(datetime.now() - self.last_update_time)
        self.last_update_time = datetime.now()
		
        if isinstance(measurement, VehicleSpeed):
            #self.messages_received.append(measurement)
			print(measurement)
	
    def receive(self, message, **kwargs):
        self._update(message)
        #if message.__class__ == VehicleSpeed:
        #    print(message)
        #elif message.__class__ == Longitude:
		#    print(datetime.now().strftime("%I:%M:%S"), message)
		
 #   def printMessage(self):
 #       print(len(self.messages_received))	
		
def main():
    configure_logging()
    arguments = parse_options()
    source_class, source_kwargs = select_device(arguments)
	
    vehicle = Vehicle()
    vehicle.add_source(source_class(**source_kwargs))
    test = VehicleTest(vehicle)
    while True:
	time.sleep(1)
	
    #vehicle.listen(Measurement, receive)
	
    #message_id = 42
    #mode = 1
    #vi.create_diagnostic_request(message_id, mode, bus=1, pid=3, wait_for_first_response=True)
    #vi.write(bus=1, id=42, da="0x1234567812345678")
    #vi.set_passthrough(1, True)

main()
