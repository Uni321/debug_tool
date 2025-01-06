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

command = control_command_pb2.ControlCommand()

def ParseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file_path", type=str, default="")
    parser.add_argument("-s", "--start_time", type=float, default="0")
    parser.add_argument("-e", "--end_time", type=float, default="0")

    args = parser.parse_args()
    return args

def debug_control(args):
    bag = rosbag.Bag(args.file_path)

    car_state_speed = []
    angle = []
    lateral_error = []
    heading_error = []
    target_speed = []
    path_acc = []
    acc_ff = []
    acc_fb = []
    acc_compensation = []
    acc_command = []

    throttle = []
    brake = []
    brake_stand_still = []

    for topic, msg, t in bag.read_messages(topics=['/control/control_command', '/blrobot/canbus/control_msgs']):
        if args.start_time != 0 and t.to_sec() < args.start_time:
            continue
        if args.end_time != 0 and t.to_sec() > args.end_time:
            continue
        if topic == '/control/control_command':
            command.ParseFromString(msg.data)
            if not command.HasField("angle"):
                continue
            car_state_speed.append(command.simple_debug.speed)
            angle.append(command.angle)
            lateral_error.append(command.simple_debug.lateral_error)
            heading_error.append(command.simple_debug.heading_error)
            target_speed.append(command.simple_debug.speed_reference)
            path_acc.append(command.simple_debug.acceleration_reference)
            acc_ff.append(command.simple_debug.acceleration_lookup)
            acc_fb.append(command.simple_debug.acceleration_feedback)
            acc_compensation.append(command.simple_debug.heading_acceleration)
            acc_command.append(command.acceleration)
        elif topic == '/blrobot/canbus/control_msgs':
            throttle.append(msg.throttle)
            brake.append(msg.brake)
            brake_stand_still.append(msg.brake_stand_still)


    bag.close()

    x = np.arange(len(target_speed))
    fig, axes = plt.subplots(nrows=2, ncols=1)

    axes[1].plot(x, path_acc, label='path acc')
    axes[1].plot(x, acc_ff, label='acc ff')
    axes[1].plot(x, acc_fb, label='acc fb')
    axes[1].plot(x, acc_compensation, label='acc_compensation')
    axes[1].plot(x, acc_command, label='acc command')
    axes[1].set_title('acc info')

    axes[1].plot(x, car_state_speed, label='car state speed')
    axes[1].plot(x, target_speed, label='target speed')

    x2 = np.arange(len(throttle))
    axes[0].plot(x2, throttle, label='throttle')
    axes[0].plot(x2, brake, label='brake')
    axes[0].plot(x2, brake_stand_still, label='standstill')
    axes[0].set_title('bus control')

    plt.legend()
    plt.show()


if __name__ == '__main__':
  args = ParseArgs()
  tester = debug_control(args)
