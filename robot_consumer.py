# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 14:14:21 2021

@author: hoathi
"""

import robot_common
import arrowhead_client.client.core_service_forms.client as forms
import time

from client_python.arrowhead_client.client.implementations import SyncClient
from arrowhead_client.client.core_services import CoreServices
from arrowhead_client.data import BaseData, SensorData, Data
from json import dumps

import threading

robot_consumer = SyncClient.create(
        system_name='robot_consumer',
        address='localhost',
        port=6000,
        keyfile='certificates/robot_consumer.key',
        certfile='certificates/robot_consumer.crt',
        cafile='certificates/sysop.ca',)
robot_consumer_mgmt = SyncClient.create(
        system_name='robot_consumer_mgmt',
        address='localhost',
        port=6001,
        keyfile='certificates/sysop.key',
        certfile='certificates/sysop.crt',
        cafile='certificates/sysop.ca',)

service_definition = 'temp_service_definition'

def sendOrchestrationStoreEntry(client, provider, address, port, interface):
    response = client.consume_service_raw(
                CoreServices.ORCHESTRATION_POST_STORE,
                json=[
                      {
                        "serviceDefinitionName": service_definition,
                        "consumerSystemId": 23,
                        "providerSystem": {
                          "systemName": provider,
                          "address": address,
                          "port": port
                        },
                        "serviceInterfaceName": interface,
                        "priority": 1
                      }
                    ])
    print(response) 

    
if __name__ == '__main__':
    robot_consumer.setup()
    robot_consumer_mgmt.setup()
    
    #Consumer services
    
    rules = robot_consumer.add_orchestration_rule(service_definition, 'GET')
    print("RULES", rules[0].system_name, rules[0].endpoint, rules[0].interface.dto())

    sendOrchestrationStoreEntry(robot_consumer_mgmt, 
                                rules[0].system_name, 
                                rules[0].address, 
                                rules[0].port,
                                rules[0].interface.dto())

    #response = robot_consumer.consume_service(service_definition)
    #print(response.read_json()['system_name'], response.read_json()['service_name'])
    
    #response = robot_consumer_mgmt.consume_service_raw(CoreServices.ORCHESTRATION_GET_STORE)
    #print(response)
    
    """
    consumer_thread = threading.Thread(target=consumer_function, args=([]robot_producer]))
    consumer_thread.start()
    consumer_thread.join()
    """
