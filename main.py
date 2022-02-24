import cv2
import numpy
import json
import os
import yaml
import os_module as om
import re

script_path = os.path.dirname(__file__)
os.chdir(script_path)

if __name__ == "__main__":
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    list_mp4 = om.extract_folder(config['input_path'], "mp4", True)
    
    for mp4_file in list_mp4:
        cap = cv2.VideoCapture(mp4_file)
        frame_num = 0
        
        file_name = os.path.splitext(os.path.basename(mp4_file))[0]
        output_jpg_folder = os.path.join(config['output_path'], file_name, "image")
        output_json_folder = os.path.join(config['output_path'], file_name, "json")
        if not os.path.isdir(output_jpg_folder):
            os.makedirs(output_jpg_folder)
        if not os.path.isdir(output_json_folder):
            os.makedirs(output_json_folder)
        
        while (frame_num := frame_num+1):
            ret, frame = cap.read()

            if not(ret):
                break
            
            print(f"frame number : {frame_num}")
            if frame_num % config['capture_per_frame'] == 0:
                save_name_jpg = str(frame_num).zfill(8) + ".jpg"
                save_name_json = str(frame_num).zfill(8) + ".json"
                save_dict = [{
                    "file_path": re.sub('data', 'DL_data_big', os.path.join(output_jpg_folder, save_name_jpg)),
                    "obj_id": 0,
                    "position": "0",
                    "obj_class": 0,
                    "cx": 100.0,
                    "cy": 100.0,
                    "width": 100.0,
                    "height": 200.0,
                    "radian": 0.1,
                    "xmin": 1.0,
                    "ymin": 1.0,
                    "xmax": 5.0,
                    "ymax": 5.0,
                    "head_x": 100.0,
                    "head_y": 90.0,
                    "neck_x": 150.0,
                    "neck_y": 150.0,
                    "hip_x": 180.0,
                    "hip_y": 200.0
                }]
                cv2.imwrite(os.path.join(output_jpg_folder, save_name_jpg), frame)
                file_ = open(os.path.join(output_json_folder, save_name_json), "w")
                json.dump(save_dict, file_)
                file_.close()
                        
    print("END")
