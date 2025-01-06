#!/usr/bin/python
import sys
import rospy
import argparse
import matplotlib.pyplot as plt
import numpy as np

sys.path.append('/opt/uni/control/lib/control_common/')
sys.path.append('/opt/uni/control/include/proto')
sys.path.append('/opt/uni/control/share')

import common.vehicle_state.vehicle_state_pb2 as vehicle_state_pb2
import control_command_pb2
import path_pb2
from control_common.msg import Bytes
from control_common.msg import busControl
from std_msgs.msg import String



import rosbag

car_state = vehicle_state_pb2.VehicleState()

def ParseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file_path", type=str, default="")
    parser.add_argument("-s", "--start_time", type=float, default="0")
    parser.add_argument("-e", "--end_time", type=float, default="0")

    args = parser.parse_args()
    return args

def debug_control(args):
    bag = rosbag.Bag(args.file_path)

    pitch = []

    for topic, msg, t in bag.read_messages(topics=['/canbus/car_state']):
        if args.start_time != 0 and t.to_sec() < args.start_time:
            continue
        if args.end_time != 0 and t.to_sec() > args.end_time:
            continue
        car_state.ParseFromString(msg.data)
        pitch.append(car_state.roll_pitch_yaw.y)
    bag.close()
    print('average pitch ', sum(pitch) / len(pitch))

if __name__ == '__main__':
  args = ParseArgs()
  tester = debug_control(args)
