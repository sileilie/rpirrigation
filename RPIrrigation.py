#! /usr/bin/python  
"""Watering programmer for RaspberryPi"""  

# Controls GPIO pins 5,6,13,19 connected trough relays to 4 waterring electrovalves  
# Version 3, approach with schedule and gpiozero output device
# Last update: 25.11.2022
# by Vasile Ilie (sileilie@gmail.com)  

import gpiozero
import datetime
import yaml
import schedule
import logging
import sys

logging.basicConfig(filename='irrigation.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')

#Reads yaml config file to "irrigation_conf" dict object ; if something fishy exit with exitcode 1 & log & message
with open("irrigation_config.yml", "r") as stream:
    try:
        irrigation_conf=yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logging.info('%s yaml file issue:', exc) #add info to log
        print(exc)
        sys.exit(1)

# Define valves start and run time variables extracting values from dict object irrigation_conf
valve_1_ontime = irrigation_conf.get('Valve_1').get('ON_time')
valve_1_runtime = irrigation_conf.get('Valve_1').get('RUN_time')
valve_2_ontime = irrigation_conf.get('Valve_2').get('ON_time')
valve_2_runtime = irrigation_conf.get('Valve_2').get('RUN_time')
valve_3_ontime = irrigation_conf.get('Valve_3').get('ON_time')
valve_3_runtime = irrigation_conf.get('Valve_3').get('RUN_time')
valve_4_ontime = irrigation_conf.get('Valve_4').get('ON_time')
valve_4_runtime = irrigation_conf.get('Valve_4').get('RUN_time')

#Define pins to control valves ralays
valve1_pin = 5  # pin number for relay 1, valve 1
valve2_pin = 6  # pin number for relay 2, valve 2
valve3_pin = 13  # pin number for relay 3, valve 3
valve4_pin = 19   # pin number for relay 4, valve 4 

#Define gpio valve objects:
valve_1 = gpiozero.OutputDevice(valve1_pin, active_high=False, initial_value=False)
valve_2 = gpiozero.OutputDevice(valve2_pin, active_high=False, initial_value=False)
valve_3 = gpiozero.OutputDevice(valve3_pin, active_high=False, initial_value=False)
valve_4 = gpiozero.OutputDevice(valve4_pin, active_high=False, initial_value=False)

#Define irrigation function - open a specific valve for a specific durration in seconds
def irrigation(valve, duration):    # funcion to open valve for a specific duration in seconds and then close it
#try
#if valve.value = low
    valve.on()
    logging.info('%s started', valve) #add info to log
    time.sleep(duration)
    valve.off()
    logging.info('%s closed', valve) #add info to log
#exceptia


# Schedule to open a sppecific valve for a specific time at a specific hour
# !ATT not to overlap between valvesin config file ! set the second valve time on after the first valve time on + pause interval!!!!
# If both valves are open in the same time the water pressure will drop and the wattering will not be effective!)
schedule.every().day.at("valve_1_ontime").do(irrigation, valve=valve_1, duration=int(valve_1_runtime)) 
schedule.every().day.at("valve_2_ontime").do(irrigation, valve=valve_2, duration=int(valve_2_runtime))
#schedule.every().day.at("valve_3_ontime").do(irrigation, valve=valve_1, duration=int(valve_3_runtime)) 
#schedule.every().day.at("valve_4_ontime").do(irrigation, valve=valve_2, duration=int(valve_4_runtime))

# Run pending scheduled tasks every 5 seconds: 
while True:
    schedule.run_pending()
    time.sleep(5)
