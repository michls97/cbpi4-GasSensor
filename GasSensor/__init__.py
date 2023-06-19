# -*- coding: utf-8 -*-
import asyncio
import random
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from cbpi.api import parameters, CBPiSensor


i2c = busio.I2C(1, 0)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P3)

@parameters([Property.Actor(label="Actor",  description="Select the actor that will be switched on/off depending on the threshold"),
            Property.Number(label="Threshold", configurable=True,  description="Threshold value of gas concentration; Higher: Actor switches on/off"),
            Property.Select(label="SwitchType", options=["On", "Off"],description="On: Actor will be switched on; Off: Actor will be switched off"),])

class GasSensor(CBPiSensor):

    def __init__(self, cbpi, id, props):
        super(GasSensor, self).__init__(cbpi, id, props)
        self.value = 0
        self.threshold = self.props.get("Threshold", 1000)

    async def run(self):
        while self.running:
            self.value = chan.value
            self.log_data(self.value)
            self.push_update(self.value)
            
            if self.notification == "Yes":
                    self.cbpi.notify("Gas Sensor", "Gasbrenner switched off as Gas Sensor above {}".format(self.threshold), NotificationType.INFO)
            await asyncio.sleep(1)

    def get_state(self):
        return dict(value=self.value)


def setup(cbpi):
    '''
    This method is called by the server during startup
    Here you need to register your plugins at the server

    :param cbpi: the cbpi core
    :return:
    '''
    cbpi.plugin.register("GasSensor", GasSensor)

