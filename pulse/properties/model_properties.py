import json
import os
from dataclasses import dataclass

from pulse import app
from pulse.properties.material import Material
from pulse.properties.fluid import Fluid
# from vibra.project.project_file import *

from numpy import ndarray


DEFAULT_MATERIAL = Material(
    name="Steel",
    identifier=1,
    color=(200, 200, 200),
    density=7860,
    elasticity_modulus=210e9,
    poisson_ratio=0.3,
)

DEFAULT_FLUID = Fluid(
    name="Air",
    identifier=1,
    color=(200, 200, 200),
    density=1.215,
    speed_of_sound=343.2021,
)


class ModelProperties:
    """
    Class that stores all properties of a model.

    All properties can be setted per node, element, entity,
    volume or globally.

    The only functions that deals with data are _set_property,
    _get_property and _reset_property. All the others are just
    wrappers that call these ones.

    I know it may seem a little weird to structure the data this
    way because it would probably be faster to just use one dict
    for each property in each level of the structure.
    But the current approach is (I hope) a lot less error prone.
    It uses few dicts and we do not need to care if the data
    is handled correctly for each case, because few functions
    handles it, reducing the points of failure.

    Also, the speed is only a requirement on the retrieval of
    data (because it is done multiple times by every element),
    and it is pretty fast. The other operations are proportional
    to things that a human can put here manually (and by the real
    world requirements of the model), so of course a computer can
    handle it in fractions of a second.

    """

    def __init__(self, model=None):
        # self.file = ProjectFile()
        self._reset_variables()

    def _reset_variables(self):

        self.acoustic_imported_tables = dict()
        self.structural_imported_tables = dict()

        self.global_properties = dict()
        self.group_properties = dict()
        self.line_properties = dict()
        self.element_properties = dict()
        self.nodal_properties = dict()

        self.global_properties["material", "global"] = DEFAULT_MATERIAL
        self.global_properties["fluid", "global"] = DEFAULT_FLUID

    def add_imported_tables(self, group_label : str, table_name : str, data : ndarray | list | tuple):
        if group_label == "acoustic":
            self.acoustic_imported_tables[table_name] = data
        elif group_label == "structural":
            self.structural_imported_tables[table_name] = data

    def remove_imported_tables(self, group_label : str, table_name : str):
        if group_label == "acoustic":
            if table_name in self.acoustic_imported_tables.keys():
                self.acoustic_imported_tables.pop(table_name)
        elif group_label == "structural":
            if table_name in self.structural_imported_tables.keys():
                self.structural_imported_tables.pop(table_name)

    def get_material(self, **kwargs) -> Material:
        return self._get_property("material", **kwargs)

    def get_fluid(self, **kwargs) -> Fluid:
        return self._get_property("fluid", **kwargs)

    def get_dissipation_model(self, **kwargs):
        return self._get_property("dissipation_model", **kwargs)
    
    def get_lrf_model_inputs(self, element_id):
        return self._get_property("lrf_eq_model", element=element_id)

    def set_material(self, material: Material, line=None, element=None):
        self._set_property("material", material, line=line, element=element)

    def set_fluid(self, fluid: Fluid, line=None, element=None):
        self._set_property("fluid", fluid, line=line, element=element)

    # def get_fluid_density(self, fluid, **kwargs):
    #     rho_0 = fluid.fluid_density
    #     dissipation_model = self.get_dissipation_model(**kwargs)
    #     if dissipation_model is None:
    #         return rho_0
    #     elif dissipation_model["model"] == "proportional damping":
    #         factor = dissipation_model["fluid density factor"]
    #         return (1 + factor * 1j) * rho_0

    # def get_speed_of_sound(self, fluid, **kwargs):
    #     c_0 = fluid.speed_of_sound
    #     dissipation_model = self.get_dissipation_model(**kwargs)
    #     if dissipation_model is None:
    #         return c_0
    #     elif dissipation_model["model"] == "proportional damping":
    #         factor = dissipation_model["speed of sound factor"]
    #         return (1 + factor * 1j) * c_0

    def get_prescribed_dofs(self, node_ids):
        return self._get_property("prescribed_dofs", node_ids=node_ids)

    def get_nodal_loads(self, node_ids):
        return self._get_property("nodal_loads", node_ids=node_ids)

    def set_prescribed_dofs(self, data, node_ids):
        self._set_property("prescribed_dofs", data, node_ids)

    def set_nodal_loads(self, data, node_ids):
        self._set_property("nodal_loads", data, node_ids)

    def set_structural_elastic_links(self, data, node_ids):
        self._set_property("prescribed_dofs", data, node_ids)

    def get_acoustic_pressure(self, node_ids):
        return self._get_property("acoustic_pressure", node_ids=node_ids)

    def get_volume_velocity(self, node_ids):
        return self._get_property("volume_velocity", node_ids=node_ids)

    def get_specific_impedance(self, node_ids):
        return self._get_property("specific_impedance", node_ids=node_ids)

    def get_radiation_impedance(self, node_ids):
        return self._get_property("radiation_impedance", node_ids=node_ids)

    def set_acoustic_pressure(self, data, node_ids):
        self._set_property("acoustic_pressure", data, node_ids=node_ids)

    def set_volume_velocity(self, data, node_ids):
        self._set_property("volume_velocity", data, node_ids=node_ids)

    def set_specific_impedance(self, data, node_ids):
        self._set_property("specific_impedance", data, node_ids=node_ids)

    def set_radiation_impedance(self, data, node_ids):
        self._set_property("radiation_impedance", data, node_ids=node_ids)

    def get_data_group_label(self, property : str):
        if property in ["acoustic_pressure", "volume_velocity", "specific_impedance", "radiation_impedance", "compressor_excitation"]:
            return "acoustic"
        else:
            return "structural"

    def _set_property(self, property: str, data, node_ids=None, element=None, line=None, group=None):
        """
        Sets a data to a property by node, element, line, surface or volume
        if any of these exists. Otherwise sets the property as global.

        """

        if node_ids is not None:

            group_label = self.get_data_group_label(property)

            values = list()
            if "real values" in data.keys() and "imag values" in data.keys():
                for i, a in enumerate(data["real values"]):
                    if a is None:
                        values.append(None)
                    else:
                        b = data["imag values"][i]
                        values.append(a + 1j*b)
            
            if "table names" in data.keys():

                if group_label == "acoustic":
                    imported_tables = self.acoustic_imported_tables
                else:
                    imported_tables = self.structural_imported_tables

                for i, table_name in enumerate(data["table names"]):

                    if table_name is None:
                        values.append(None)
                        continue

                    if table_name in imported_tables.keys():

                        data_array = imported_tables[table_name]
                        value = data_array[:, 1] + 1j*data_array[:, 2]
                        values.append(value)

            data["values"] = values

            if isinstance(node_ids, int):
                self.nodal_properties[property, node_ids] = data

            elif isinstance(node_ids, list) and len(node_ids) == 2:
                self.nodal_properties[property, node_ids[0], node_ids[1]] = data

        elif element is not None:
            self.element_properties[property, element] = data

        elif line is not None:
            self.line_properties[property, line] = data

        elif group is not None:
            self.group_properties[property, group] = data

        # else:
        #     self.global_properties[property, "global"] = data

    def _get_property(self, property: str, node_ids=None, element=None, line=None):
        """
        Finds the value that corresponds to the property needed.
        Checks node, element, entity, volume and global data by
        this respective order of priority.
        If the any of this is defined returns None.
        """

        if isinstance(node_ids, int):
            if (property, node_ids) in self.nodal_properties:
                return self.nodal_properties[property, node_ids]

        elif isinstance(node_ids, list) and len(node_ids) == 2:
            if (property, node_ids[0], node_ids[1]) in self.nodal_properties:
                return self.nodal_properties[property, node_ids[0], node_ids[1]]

        if (property, element) in self.element_properties:
            return self.element_properties[property, element]

        if (property, line) in self.line_properties:
            return self.line_properties[property, line]

        if (property, "global") in self.global_properties:
            return self.global_properties[property, "global"]

        return None

    def check_if_there_are_tables_at_the_model(self):
        """This method checks if there are imported table of values in
        the model. It returns True if exists or False elsewhere.
        """

        data_dicts = [
                        self.nodal_properties,
                        self.element_properties,
                        self.line_properties,
                        self.global_properties,
                     ]

        for data_dict in data_dicts:
            for data in data_dict.values():
                if isinstance(data, dict):
                    if "table_name" in data.keys():
                        return True

        return False

    def _reset_property(self, property: str):
        """
        Clears all instances of a specific property from the structure.
        """
        data_dicts = [  self.nodal_properties,
                        self.element_properties,
                        self.line_properties,
                        self.group_properties,
                        self.global_properties  ]

        for data in data_dicts:
            keys_to_remove = []

            for key in data.keys():
                if len(key) == 2:
                    existing_property, _ = key
                else:
                    existing_property = key

                if property == existing_property:
                    keys_to_remove.append(key)

            for _key in keys_to_remove:
                data.pop(_key)

    def _remove_nodal_property(self, property: str, node_id: int):
        """Remove a nodal property at specific nodal_id."""
        key = (property, node_id)
        if key in self.nodal_properties.keys():
            self.nodal_properties.pop(key)

    def _remove_element_property(self, property: str, element_id: int):
        """Remove a element property at specific element_id."""
        key = (property, element_id)
        if key in self.element_properties.keys():
            self.element_properties.pop(key)

    def _remove_line_property(self, property: str, line_id: int):
        """Remove a line property at specific line_id."""
        key = (property, line_id)
        if key in self.line_properties.keys():
            self.line_properties.pop(key)

    def _remove_group_property(self, property: str, group_id: int):
        """Remove a group property at specific group_id."""
        key = (property, group_id)
        if key in self.group_properties.keys():
            self.group_properties.pop(key)

    def get_nodal_related_table_names(self, property : str, node_ids : list | tuple, equals = False) -> list:
        table_names = list()
        for key, data in self.nodal_properties.items():
            for node_id in node_ids:

                if "table names" in data.keys():
                    if equals:
                        if key == (property, node_id):
                            for table_name in data["table names"]:
                                if table_name is not None:
                                    table_names.append(table_name)

                    else:
                        if key != (property, node_id):
                            if key[1] == node_id:
                                for table_name in data["table names"]:
                                    if table_name is not None:
                                        table_names.append(table_name)

        return table_names

    def get_element_related_table_names(self, property : str, element_ids : list | tuple, equals = False):
        table_names = dict()
        for key, data in self.element_properties.items():
            for element_id in element_ids:
                if "table names" in data.keys():
                    if equals:
                        if key == (property, element_id):
                            table_names[key] = data["table names"]
                    else:
                        if key == (property, element_id):
                            continue
                        else:
                            if key[1] == element_id:
                                table_names[key] = data["table names"]
        return table_names

if __name__ == "__main__":
    p = ModelProperties()
    with open("teste.json", "w") as file:
        file.write(p.as_json())

    q = ModelProperties()
    with open("teste.json", "r") as file:
        data = json.load(file)
        q.load_json(data)