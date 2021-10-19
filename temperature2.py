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
temp2_producer = SyncClient.create(system_name='temperature2',
                               address='localhost',
                               port=1438,
                               keyfile='certificates/temperature2.key',
                               certfile='certificates/temperature2.crt',
                               cafile='certificates/sysop.ca')

@temp2_producer.provided_service(
        service_definition='temperature2_service',
        service_uri='temp1',
        protocol='HTTP',
        method='GET',
        payload_format='JSON',
        access_policy='TOKEN', )

def get_temp_function(request):
    return {"system_name": "temperature2", "service_name": "temperature2_service", "type": "proxy"}


def service_function(producer):
    producer.run_forever()

#===================================Data======================================
def temp_function(mu, sigma, start_time, consumer):
    while(True):
        if keyboard.is_pressed('x'):  # if key 'q' is pressed 
            break  # finishing the loop
        
        current_time = time.time()*1000
        t = random.gauss(mu, sigma)*100
        response_t  = temp2_producer.consume_service_raw(
                   CoreServices.PROXY_PUT_DATA('temperature2', 'temperature2_service'),
                   json=[{
                        "bn": "temp2_sensor",
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
        time.sleep(4)

#===================================Mains=====================================
if __name__ == '__main__':
    temp2_producer.setup()
    
    
    start_time = time.time()*1000
    
    data_thread = threading.Thread(target=temp_function, args=(0,0.1,start_time,temp2_producer))
    data_thread.start()
    
    #temp2_producer.run_forever()
    
    data_thread.join()
    