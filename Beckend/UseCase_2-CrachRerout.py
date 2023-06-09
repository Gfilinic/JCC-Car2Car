import time
import paho.mqtt.client as paho
from paho import mqtt
import time
import math
import threading
def simulate_car_movement(lat1, lon1, lat2, lon2, speed, carID):
  
    R = 6371 # radius of Earth in kilometers

    dLat = math.radians(lat2-lat1)
    dLon = math.radians(lon2-lon1)
  

    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2) 
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
    distance = R * c * 1000 # distance in meters

    duration = distance / speed # duration in seconds
   
    
    start_time = time.time()
    current_time = start_time
    while current_time - start_time <= duration:
        elapsed_time = current_time - start_time
        fraction_of_trip = elapsed_time / duration
        current_lat = lat1 + (lat2 - lat1) * fraction_of_trip
        current_lon = lon1 + (lon2 - lon1) * fraction_of_trip
        print(f'Current location: {current_lat}, {current_lon}')
        message = f"{carID},{current_lat},{current_lon}"
        client.publish(f"LOCATION/{carID}",message)
        time.sleep(0.5)
        current_time = time.time()
    
    
def simulate_car_movement_crash(lat1, lon1, lat2, lon2, speed, carID):
  
    R = 6371 # radius of Earth in kilometers

    dLat = math.radians(lat2-lat1)
    dLon = math.radians(lon2-lon1)
  

    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2) 
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
    distance = R * c * 1000 # distance in meters

    duration = distance / speed # duration in seconds
   
    
    start_time = time.time()
    current_time = start_time
    while current_time - start_time <= duration:
        elapsed_time = current_time - start_time
        fraction_of_trip = elapsed_time / duration
        current_lat = lat1 + (lat2 - lat1) * fraction_of_trip
        current_lon = lon1 + (lon2 - lon1) * fraction_of_trip
        print(f'Current location: {current_lat}, {current_lon}')
        message = f"{carID},{current_lat},{current_lon}"
        client.publish(f"LOCATION/{carID}",message)
        time.sleep(0.5)
        current_time = time.time()
    rlat2 = round(lat2, 2)
    rlon2 = round(lon2, 2)
    
    client.publish("DANGER",f"Car Crashed! Location: {str(rlat2)}, {str(rlon2)}" )
    
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect


client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("JCC_RC_CommunicationFramework", "@B1EfbPKD%Pp%kPG")
client.connect("e5c6690c23234ff8b2e11e59d3fb82be.s2.eu.hivemq.cloud", 8883)

def simulate_car_movement_reroute():
  
   simulate_car_movement(46.297928, 16.340842, 46.298675, 16.340446, 40, 8)
   time.sleep(5)
   simulate_car_movement(46.298858, 16.340304, 46.303714, 16.337721, 40, 8)

client.subscribe("LOCATION/#", qos=1)

def main():
    time.sleep(7)
    t1 = threading.Thread(target=simulate_car_movement_crash, args=(46.298482, 16.336989, 46.299213, 16.336894, 50, 7))
    t2 = threading.Thread(target=simulate_car_movement_reroute)
    
   
    t1.start()
    time.sleep(1.25)
    t2.start()
    t2.join()
    
    
 
   
  
    
    
    
if __name__=="__main__":
    main()