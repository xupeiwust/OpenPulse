from opps.model.pipe import Pipe
from opps.model.bend import Bend
from opps.model.flange import Flange

from pulse.utils import m_to_mm, in_to_mm
import numpy as np

import sys
import gmsh


class GMSHGeometryHandler:
    def __init__(self):
        self._initialize()

    def _initialize(self):
        self.unit = "meter"
        self.pipeline = list()

    def set_pipeline(self, pipeline):
        self.pipeline = pipeline

    def set_unit_of_length(self, unit):
        if unit in ["meter", "milimiter", "inch"]:
            self.unit = unit

    def create_geometry(self):
        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Terminal",0)
        gmsh.option.setNumber("General.Verbosity", 0)
        for structure in self.pipeline.structures: 

            if isinstance(structure, Pipe):
                
                _start_coords = structure.start.coords()
                _end_coords = structure.end.coords()
                
                if self.unit == "meter":
                    start_coords = m_to_mm(_start_coords)
                    end_coords = m_to_mm(_end_coords)
                
                elif self.unit == "inch":
                    start_coords = in_to_mm(_start_coords)
                    end_coords = in_to_mm(_end_coords)

                start_point = gmsh.model.occ.add_point(*start_coords)
                end_point = gmsh.model.occ.add_point(*end_coords)

                gmsh.model.occ.add_line(start_point, end_point)

            elif isinstance(structure, Bend):
                if structure.is_colapsed():
                    continue
                
                _start_coords = structure.start.coords()
                _end_coords = structure.end.coords()
                _center_coords = structure.center.coords()

                if self.unit == "meter":
                    start_coords = m_to_mm(_start_coords)
                    end_coords = m_to_mm(_end_coords)
                    center_coords = m_to_mm(_center_coords)
                
                elif self.unit == "inch":
                    start_coords = in_to_mm(_start_coords)
                    end_coords = in_to_mm(_end_coords)
                    center_coords = in_to_mm(_center_coords)

                start_point = gmsh.model.occ.add_point(*start_coords)
                end_point = gmsh.model.occ.add_point(*end_coords)
                center_point = gmsh.model.occ.add_point(*center_coords)

                gmsh.model.occ.add_circle_arc(start_point, center_point, end_point)

        gmsh.model.occ.synchronize()
        # if '-nopopup' not in sys.argv:
        #     gmsh.option.setNumber('General.FltkColorScheme', 1)
        #     gmsh.fltk.run()
        # # gmsh.write(str(path))
        # gmsh.finalize()