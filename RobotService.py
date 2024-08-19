import json
import os
import numpy as np
import torch
from ultralytics import YOLO
from PIL import Image
from grasp_generator import GraspGenerator
from environment.utilities import Camera
from environment.env import Environment
from utils import YcbObjects
import pybullet as p
import argparse
import sys
from LLMManager import LLMManager
from YOLOService import YOLOService
from SimulationService import SimulationService
from VoiceToTextService import OpenAIVoiceToTextService

sys.path.append('network')

class RobotService:

    class_names = [
        '003_cracker_box', '004_sugar_box', '005_tomato_soup_can', '006_mustard_bottle', '007_tuna_fish_can',
        '008_pudding_box', '009_gelatin_box', '010_potted_meat_can', '011_banana', '019_pitcher_base',
        '021_bleach_cleanser', '024_bowl', '025_mug', '035_power_drill', '036_wood_block',
        '037_scissors', '040_large_marker', '051_large_clamp', '052_extra_large_clamp', '061_foam_brick'
    ]
    
    def __init__(self):
        self.args = self.parse_args()

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Grasping demo')
        parser.add_argument('--scenario', type=str, default='pack', help='Grasping scenario (pack)')
        parser.add_argument('--runs', type=int, default=1, help='Number of runs the scenario is executed')
        parser.add_argument('--show-network-output', dest='output', type=bool, default=False, help='Show network output (True/False)')
        return parser.parse_args()

    def load_yolo_model(self, weights_file):
        model = YOLO(weights_file)
        return model

    def Configure(self, vis, debug):

        self.simulationService = SimulationService()
        self.simulationService.Configure()

        self.yoloService = YOLOService()
        self.yoloService.Configure("yolo5.pt", self.class_names)


    def PerformTask(self, detected_objects):
        user_input = self.stt.GetText()
        self.response = LLMManager().process_input(user_input, detected_objects)

    def grasp(self):

        rgb, depth = self.simulationService.GetImage()
        
        self.detected_objects, self.boxes = self.yoloService.RecognizeObjects(rgb)
        self.simulationService.grasp_test(5, True, None, self.detected_objects, self.boxes)

def main():
    robotService = RobotService()
    args = robotService.parse_args()
    output = args.output
    runs = args.runs
    robotService.Configure(vis=True, debug=False)
    robotService.grasp()

if __name__ == '__main__':
    main()
