import os
import numpy as np
import pybullet as pb
from grasp_generator import GraspGenerator
from environment.utilities import Camera
from environment.env import Environment
from utils import YcbObjects
from LLMManager import LLMManager
import json
from YOLOService import YOLOService

class SimulationService:

    class_names = [
        '003_cracker_box', '004_sugar_box', '005_tomato_soup_can', '006_mustard_bottle', '007_tuna_fish_can',
        '008_pudding_box', '009_gelatin_box', '010_potted_meat_can', '011_banana', '019_pitcher_base',
        '021_bleach_cleanser', '024_bowl', '025_mug', '035_power_drill', '036_wood_block',
        '037_scissors', '040_large_marker', '051_large_clamp', '052_extra_large_clamp', '061_foam_brick'
    ]

    def Configure(self, vis=True, debug=False):

        self.objects = YcbObjects('objects/ycb_objects', mod_orn=['ChipsCan', 'MustardBottle', 'TomatoSoupCan'], mod_stiffness=['Strawberry'])
        center_x, center_y = 0.05, -0.52
        self.network_path = 'network/trained-models/cornell-randsplit-rgbd-grconvnet3-drop1-ch32/epoch_19_iou_0.98'
        self.camera = Camera((center_x, center_y, 1.9), (center_x, center_y, 0.785), 0.2, 2.0, (224, 224), 40)
        self.env = Environment(self.camera, vis=vis, debug=debug, finger_length=0.06)
        self.generator = GraspGenerator(self.network_path, self.camera, 5)

        self.yoloService = YOLOService()
        self.yoloService.Configure("yolo5.pt", self.class_names)

        info = self.objects.get_n_first_obj_info(5)
        self.env.create_packed(info)

    def GetImage(self) -> tuple:
            
            rgb, depth, _ = self.camera.get_cam_img()
            return rgb, depth
    
    def grasp_test(self, n, vis, output, detected_objects, boxes):

        for i in range(n):
            print(f'Trial {i}')
            
            object_names = ['005_tomato_soup_can', '011_banana', '009_gelatin_box', '035_power_drill', '037_scissors']  

            while len(self.env.obj_ids) != 0:

                #reset
                self.env.move_away_arm()
                self.env.reset_all_obj()

                #get info from camera
                rgb, depth, _ = self.camera.get_cam_img()

                # Generate grasps
                grasps, save_name = self.generator.predict_grasp(rgb, depth, n_grasps=3, show_output=output)

                #detected_objects, boxes = self.yoloService.RecognizeObjects(rgb)

                prompt = input("How can I help you?")
                response = LLMManager().process_input(prompt, detected_objects)
                print(response)
                grasping = json.loads(response)['commands']
                print(grasping)

                for item in grasping:
                    if item['command'] == "GRASP_OBJECT":
                        for i, grasp in enumerate(grasps):
                            x, y, z, roll, opening_len, obj_height = grasp

                            # Find the closest bounding box center
                            min_distance = float('inf')
                            closest_box = None
                            for box in boxes:
                                box_x_center = float((box[0] + box[2]) / 2)
                                box_y_center = float((box[1] + box[3]) / 2)
                                box_x_center, box_y_center = self.generator.bb_to_robot_frame((box_x_center, box_y_center))
                                distance = np.linalg.norm([x - box_x_center, y - box_y_center])

                                if distance < min_distance:
                                    min_distance = distance
                                    closest_box = box
                                print(min_distance, int(closest_box[5]))
                            if closest_box is not None:
                                class_id = int(closest_box[5])  # Convert class ID to int
                                confidence = closest_box[4]

                                # Map class ID to class name
                                class_name = self.class_names[class_id]
                                print(f"The class name is {class_name}")

                            if class_name == item["parameters"][0]: #class_names is what YOLO found
                                if vis:
                                    debug_id = pb.addUserDebugLine([x, y, z], [x, y, 1.2], [0, 0, 1], lineWidth=3)

                                selected_object = item["parameters"][0]
                                print(f"Taking the object of name {selected_object}")
                                success_grasp, success_target = self.env.grasp((x, y, z), roll, opening_len, obj_height)

                                if vis:
                                    pb.removeUserDebugItem(debug_id)

                                if success_target:
                                    if save_name is not None:
                                        os.rename(save_name + f'_SUCCESS_grasp{i}.png')
                                    break
                                else:
                                    print(f"Failed to grasp at ({x, y, z}). Trying again...")

                self.env.reset_all_obj()

            self.env.remove_all_obj()

    def grasp(self, n, vis, output, object_name, detected_objects, boxes):

        for i in range(n):
            print(f'Trial {i}')

            while len(self.env.obj_ids) != 0:

                #reset
                self.env.move_away_arm()
                self.env.reset_all_obj()

                #get info from camera
                rgb, depth, _ = self.camera.get_cam_img()

                # Generate grasps
                grasps, save_name = self.generator.predict_grasp(rgb, depth, n_grasps=3, show_output=output)

                #detected_objects, boxes = self.yoloService.RecognizeObjects(rgb)

                # prompt = input("How can I help you?")
                # response = LLMManager().process_input(prompt, detected_objects)
                # print(response)
                # grasping = json.loads(response)['commands']
                # print(grasping)

                for i, grasp in enumerate(grasps):
                    x, y, z, roll, opening_len, obj_height = grasp

                    # Find the closest bounding box center
                    min_distance = float('inf')
                    closest_box = None
                    for box in boxes:
                        box_x_center = float((box[0] + box[2]) / 2)
                        box_y_center = float((box[1] + box[3]) / 2)
                        box_x_center, box_y_center = self.generator.bb_to_robot_frame((box_x_center, box_y_center))
                        distance = np.linalg.norm([x - box_x_center, y - box_y_center])

                        if distance < min_distance:
                            min_distance = distance
                            closest_box = box
                        print(min_distance, int(closest_box[5]))
                    if closest_box is not None:
                        class_id = int(closest_box[5])  # Convert class ID to int
                        confidence = closest_box[4]

                        # Map class ID to class name
                        class_name = self.class_names[class_id]
                        print(f"The class name is {class_name}")

                    if class_name == object_name: #class_names is what YOLO found
                        if vis:
                            debug_id = pb.addUserDebugLine([x, y, z], [x, y, 1.2], [0, 0, 1], lineWidth=3)

                        selected_object = object_name
                        print(f"Taking the object of name {selected_object}")
                        success_grasp, success_target = self.env.grasp((x, y, z), roll, opening_len, obj_height)

                        if vis:
                            pb.removeUserDebugItem(debug_id)

                        if success_target:
                            if save_name is not None:
                                os.rename(save_name + f'_SUCCESS_grasp{i}.png')
                            break
                        else:
                            print(f"Failed to grasp at ({x, y, z}). Trying again...")

                self.env.reset_all_obj()

            self.env.remove_all_obj()