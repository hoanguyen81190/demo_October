# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 14:14:21 2021

@author: hoathi
"""


from client_python.arrowhead_client.client.implementations import SyncClient
from arrowhead_client.client.core_services import CoreServices

thermostat_consumer = SyncClient.create(
        system_name='thermostat',
        address='localhost',
        port=7000,
        keyfile='certificates/thermostat.key',
        certfile='certificates/thermostat.crt',
        cafile='certificates/sysop.ca',)
thermostat_consumer_mgmt = SyncClient.create(
        system_name='thermostat_consumer_mgmt',
        address='localhost',
        port=7001,
        keyfile='certificates/sysop.key',
        certfile='certificates/sysop.crt',
        cafile='certificates/sysop.ca',)

service_definition = 'temperature1_service'

def sendOrchestrationStoreEntry(client, provider, address, port, interface):
    response = client.consume_service_raw(
                CoreServices.ORCHESTRATION_POST_STORE,
                json=[
                      {
                        "serviceDefinitionName": service_definition,
                        "consumerSystemId": 73,
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
    thermostat_consumer.setup()
    thermostat_consumer_mgmt.setup()
    
    #Consumer services
    
    rules = thermostat_consumer.add_orchestration_rule(service_definition, 'GET')
    print("RULES", rules[0].system_name, rules[0].endpoint, rules[0].interface.dto())

    sendOrchestrationStoreEntry(thermostat_consumer_mgmt, 
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
