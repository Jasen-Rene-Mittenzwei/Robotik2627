# Imports:
from controller import Robot, GPS, Camera, Emitter, Receiver, Gyro, DistanceSensor, PositionSensor
import numpy as np
import cv2
import math
import struct
import os

# Var:
timeStep:int = 32       # Zeit für einen Simulationsschritt 
max_velocity:float = 3  #6.27 # Maximale Geschwindigkeit des Roboters. s.Dokumentation (eig. 6,28...) 
image, r, g, b, gpsX, gpsY, gpsZ, img_l, img_c, img_r, cam_img_l, cam_img_c, cam_img_r = (None,)*13
imagePath:str = "/home/webots/Dokumente/Robotik2627-1/Image/"

# Objekte:
robot:Robot = Robot()
#cam = erkennen (s. unten)
wheel1 = robot.getDevice("wheel1 motor")   # Motor  linkes Rad
wheel2 = robot.getDevice("wheel2 motor")   # Motor rechtes Rad
rotationsSensorLinks:PositionSensor = wheel1.getPositionSensor()    # Rotationssensoren
rotationsSensorRechts:PositionSensor = wheel2.getPositionSensor()
usVorne:DistanceSensor = robot.getDevice("distance sensor1")        # US-Sensoren (0-8)
gps:GPS = robot.getDevice("gps")                    # GPS-Sensor
colorSensor = robot.getDevice("colour_sensor")  # Farb-Sensor
cam_c:Camera = robot.getDevice("camera2")
cam_r:Camera = robot.getDevice("camera3")
lidar = robot.getDevice("lidar")

# Setup:
wheel1.setPosition(float("inf"))       # Unendliche Rotation
wheel2.setPosition(float("inf"))
rotationsSensorLinks.enable(timeStep)
rotationsSensorRechts.enable(timeStep)
usVorne.enable(timeStep)        # US-Sensor
gps.enable(timeStep)                    # GPS-Sensor
colorSensor.enable(timeStep)            # Farb-Sensor
startZeit = robot.getTime()             # Startzeit für spätere Berechnungen
cam_c.enable(timeStep)
cam_r.enable(timeStep)
lidar.enable(timeStep)

while robot.step(timeStep)!=-1:
    img_r:np.ndarray = np.frombuffer(cam_r.getImage(), np.uint8).reshape((cam_r.getHeight(), cam_r.getWidth(), 4))
    i=0
    while os.path.exists(f'{imagePath}{i}.png'):
        i+=1
    print(cv2.imwrite(f'{imagePath}{i}.png', img_r))