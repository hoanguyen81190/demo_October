# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 14:05:42 2021

@author: hoathi
"""
import time

from arrowhead_client.client.implementations import SyncClient
from arrowhead_client.client.core_services import CoreServices

import threading
import random
import keyboard

#=================================Constants===================================
VERSION = 1.0

#=================================Arrowhead===================================
robot_producer = SyncClient.create(system_name='robot_producer',
                               address='localhost',
                               port=1337,
                               keyfile='certificates/robot_producer.key',
                               certfile='certificates/robot_producer.crt',
                               cafile='certificates/sysop.ca')

@robot_producer.provided_service(
        service_definition='temp_service_definition',
        service_uri='temp',
        protocol='HTTP',
        method='GET',
        payload_format='JSON',
        access_policy='TOKEN', )

def get_temp_function(request):
    return {"system_name": "robot_producer", "service_name": "temp_service", "type": "proxy"}

@robot_producer.provided_service(
        service_definition='humidity_service_definition',
        service_uri='humidity',
        protocol='HTTP',
        method='GET',
        payload_format='JSON',
        access_policy='TOKEN', )

def get_humidity_function(request):
    return {"system_name": "robot_producer", "service_name": "humidity_service", "type": "proxy"}

@robot_producer.provided_service(
        service_definition='pressure_service_definition',
        service_uri='pressure',
        protocol='HTTP',
        method='GET',
        payload_format='JSON',
        access_policy='TOKEN', )

def get_pressure_function(request):
    return {"system_name": "robot_producer", "service_name": "pressure_service", "type": "proxy"}

def service_function(producer):
    producer.run_forever()

#===================================Data======================================
def temp_function(mu, sigma, start_time, consumer):
    while(True):
        if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            break  # finishing the loop
        
        current_time = time.time()*1000
        print("current time", current_time)
        t = random.gauss(mu, sigma)*100
        response_t  = robot_producer.consume_service_raw(
                   CoreServices.PROXY_PUT_DATA('robot_producer', 'temp_service_definition'),
                   json=[{
                        "bn": "temp_sensor",
                        "bs": 0,
                        "bt": start_time,
                        "bu": "celsius",
                        "bv": 0,
                        "bver": VERSION,
                        "n": "Temperature",
                        "s": 0,
                        "t": current_time,
                        "u": "celsius",
                        "ut": 0,
                        "v": t,
                        "vb": True,
                        "vd": "",
                        "vs": str(t)
                      }])
        print(response_t)
        
        h = random.gauss(mu, sigma)*100
        response_h = robot_producer.consume_service_raw(
                   CoreServices.PROXY_PUT_DATA('robot_producer', 'humidity_service_definition'),
                   json=[{
                        "bn": "humidity_sensor",
                        "bs": 0,
                        "bt": start_time,
                        "bu": "Percentage",
                        "bv": 0,
                        "bver": VERSION,
                        "n": "Humidity",
                        "s": 0,
                        "t": current_time,
                        "u": "Percentage",
                        "ut": 0,
                        "v": h,
                        "vb": True,
                        "vd": "",
                        "vs": str(h)
                      }])
        print(response_h)
        
        p = random.gauss(mu, sigma)*100
        response_p = robot_producer.consume_service_raw(
                   CoreServices.PROXY_PUT_DATA('robot_producer', 'pressure_service_definition'),
                   json=[{
                            "bn": "pressure_sensor",
                            "bs": 0,
                            "bt": start_time,
                            "bu": "Pa",
                            "bv": 0,
                            "bver": VERSION,
                            "n": "Pressure",
                            "s": 0,
                            "t": current_time,
                            "u": "Pa",
                            "ut": 0,
                            "v": p,
                            "vb": True,
                            "vd": "",
                            "vs": str(p)
                          }])
        print(response_p)
        time.sleep(4)

#===================================Mains=====================================
if __name__ == '__main__':
    robot_producer.setup()
    
    """
    service_thread = threading.Thread(target=service_function, args=([robot_producer]))
    service_thread.start()
    service_thread.join()
    """
    
    start_time = time.time()*1000
    
    data_thread = threading.Thread(target=temp_function, args=(0,0.1,start_time,robot_producer))
    data_thread.start()
    
    #robot_producer.run_forever()
    
    data_thread.join()
    