from pulse import app
from pulse.tools.utils import *

import os
import configparser
import numpy as np
from pathlib import Path

class PulsationSuppressionDevice:
    def __init__(self, project):

        self.project = project
        self.file = project.file

        self._initialize()
    

    def _initialize(self):
        self.pulsation_suppression_device = dict()

    def add_pulsation_suppression_device(self, device_label, suppression_device_data):

        aux = self.pulsation_suppression_device.copy()
        for key, data in aux.items():
            if data == suppression_device_data:
                self.pulsation_suppression_device.pop(key)
                break

        self.pulsation_suppression_device[device_label] = suppression_device_data
        self.write_suppression_device_data_in_file()

    def remove_suppression_device(self, device_label):

        if device_label in self.pulsation_suppression_device.keys():
            self.pulsation_suppression_device.pop(device_label)

        self.write_suppression_device_data_in_file()

    def write_suppression_device_data_in_file(self):
    
        project_path = Path(self.file._project_path)
        path = project_path / "psd_info.dat"

        config = configparser.ConfigParser()

        for key, data in self.pulsation_suppression_device.items():
            config[key] = data

        if list(config.sections()):
            with open(path, 'w') as config_file:
                config.write(config_file)
        else:
            os.remove(path)

    def load_suppression_device_data_from_file(self):
    
        project_path = Path(self.file._project_path)
        path = project_path / "psd_info.dat"

        if os.path.exists(path):

            config = configparser.ConfigParser()
            config.read(path)

            list_data_keys = [  "connecting coords",
                                "volume #1 parameters",
                                "volume #2 parameters",
                                "pipe #1 parameters",
                                "pipe #2 parameters",
                                "pipe #3 parameters"  ]

            for tag in config.sections():

                aux = dict()
                section = config[tag]

                for key in section.keys():
                    if key in ["main axis", "connection type", "volumes connection"]:
                        aux[key] = section[key]
                    elif key == "volumes spacing":
                        aux[key] = float(section[key])
                    elif key in list_data_keys:
                        aux[key] = get_list_of_values_from_string(section[key], int_values=False)

                if aux:
                    self.pulsation_suppression_device[tag] = aux
    
    def create_psd_dat(self):

        for key, value in self.pulsation_suppression_device.items():
            config = configparser.ConfigParser()
            inlet_pipe = dict()
            inlet_pipe = {"length": value["pipe #1 parameters"][0], 
                          "diameter": value["pipe #1 parameters"][1],
                          "wall thickness": value["pipe #1 parameters"][2],
                          "distance": value["pipe #1 parameters"][3],
                          "rotation_angle": value["pipe #1 parameters"][4]
                          }     
                   
            outlet_pipe = dict()            
            outlet_pipe = {"length": value["pipe #2 parameters"][0], 
                          "diameter": value["pipe #2 parameters"][1],
                          "wall thickness": value["pipe #2 parameters"][2],
                          "distance": value["pipe #2 parameters"][3],
                          "rotation_angle": value["pipe #2 parameters"][4]
                          }            
            
            main_chamber = dict()
            main_chamber = {"length": value["volume #1 parameters"][0], 
                          "diameter": value["volume #1 parameters"][1],
                          "wall thickness": value["volume #1 parameters"][2]
                            }

            config["1"] = {}
            config["1"]["start point"] = str(np.array(value["connecting coords"]) - np.array([inlet_pipe["distance"], inlet_pipe["length"], 0]))
            config["1"]["end point"] = str(np.array(value["connecting coords"]) - np.array([0, inlet_pipe["length"], 0]))

            config["2"] = {}
            config["2"]["start point"] = str(np.array(value["connecting coords"]) - np.array([0, inlet_pipe["length"], 0]))
            config["2"]["end point"] = str(np.array(value["connecting coords"]) )

            config["3"] = {}
            config["3"]["start point"] = str(np.array(value["connecting coords"]) - np.array([0, inlet_pipe["length"], 0]))
            config["3"]["end point"] = str(np.array(value["connecting coords"]) + np.array([outlet_pipe["distance"] - inlet_pipe["distance"], -inlet_pipe["length"], 0]))

            config["4"] = {}
            config["4"]["start point"] = str(np.array(value["connecting coords"]) + np.array([outlet_pipe["distance"] - inlet_pipe["distance"], -inlet_pipe["length"], 0]))
            config["4"]["end point"] = str(np.array(value["connecting coords"]) + np.array([outlet_pipe["distance"] - inlet_pipe["distance"], -inlet_pipe["length"] - outlet_pipe["length"], 0]))

            config["5"] = {}
            config["5"]["start point"] = str(np.array(value["connecting coords"]) + np.array([outlet_pipe["distance"] - inlet_pipe["distance"], -inlet_pipe["length"], 0]))
            config["5"]["end point"] = str(np.array(value["connecting coords"]) + np.array([main_chamber["length"] - outlet_pipe["distance"], -inlet_pipe["length"], 0]))

            project_path = Path(self.file._project_path)
            path = project_path / "psd_construction_info.dat"
            with open(path, 'w') as config_file:
                config.write(config_file)   