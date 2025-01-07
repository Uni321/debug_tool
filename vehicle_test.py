#!/usr/bin/python
import sys
import rospy
import argparse

sys.path.append('/opt/uni/control/lib/control_common/')
sys.path.append('/opt/uni/control/include/proto')
sys.path.append('/opt/uni/control/share')

import common.vehicle_state.vehicle_state_pb2 as vehicle_state_pb2
import control_command_pb2
import path_pb2
from control_common.msg import Bytes
from std_msgs.msg import String

topic_name_list = ['/canbus/car_state', \
                    '/planner/path', \
                    '/control/control_command']

def ParseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--topic_index", type=int, default="0", \
      help="0: /canbus/car_state \
            1: /planner/path \
            2: /control/control_command")

    args = parser.parse_args()
    return args

class vehicle_tester():
  """docstring for Vehicle"""
  def callback_car_state(self, data):
    self.car_state.ParseFromString(data.data)
    print(self.car_state)

  def callback_planner_path(self, data):
    self.path.ParseFromString(data.data)
    print(self.path)

  def callback_control_command(self, data):
    self.control_command.ParseFromString(data.data)
    print(self.control_command)


  def __init__(self, args):
    if args.topic_index < 0 or args.topic_index > len(topic_name_list) - 1:
      print('invalid topic index ', args.topic_index)
      return

    print('Subcribe topic: ', topic_name_list[args.topic_index])

    self.control_command = control_command_pb2.ControlCommand()
    self.car_state = vehicle_state_pb2.VehicleState()
    self.path = path_pb2.Path()

    rospy.init_node('tester', anonymous=True)
    if args.topic_index == 0:
      self.sub = rospy.Subscriber(topic_name_list[0], String, self.callback_car_state)
    elif args.topic_index == 1:
      self.sub = rospy.Subscriber(topic_name_list[1], Bytes, self.callback_planner_path)
    elif args.topic_index == 2:
      self.sub = rospy.Subscriber(topic_name_list[2], Bytes, self.callback_control_command)
    rospy.spin()


if __name__ == '__main__':
  args = ParseArgs()
  tester = vehicle_tester(args)
