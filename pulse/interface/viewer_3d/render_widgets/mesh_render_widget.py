import vtk
from dataclasses import dataclass
from vtkat.render_widgets import CommonRenderWidget
from vtkat.interactor_styles import BoxSelectionInteractorStyle
from vtkat.pickers import CellAreaPicker, CellPropertyAreaPicker
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from pulse.interface.viewer_3d.actors import NodesActor, ElementLinesActor, TubeActor
from pulse.interface.viewer_3d.text_helppers import TreeInfo, format_long_sequence
from pulse.interface.viewer_3d.actors.acoustic_symbols_actor import AcousticNodesSymbolsActor, AcousticElementsSymbolsActor
from pulse.interface.viewer_3d.actors.structural_symbols_actor import StructuralNodesSymbolsActor, StructuralElementsSymbolsActor
from pulse import app

@dataclass
class PlotFilter:
    nodes: bool = False
    lines: bool = False
    tubes: bool = False
    transparent: bool = False
    acoustic_symbols: bool = False
    structural_symbols: bool = False
    raw_lines: bool = False


@dataclass
class SelectionFilter:
    nodes: bool    = False
    entities: bool = False
    elements: bool = False


class MeshRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mouse_click = (0, 0)
        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)
        
        self.interactor_style = BoxSelectionInteractorStyle()
        self.render_interactor.SetInteractorStyle(self.interactor_style)

        self.open_pulse_logo = None
        self.mopt_logo = None

        self.nodes_actor = None
        self.lines_actor = None
        self.tubes_actor = None
        self.acoustic_nodes_symbols_actor = None
        self.acoustic_elements_symbols_actor = None
        self.structural_nodes_symbols_actor = None
        self.structural_elements_symbols_actor = None

        self.plot_filter = PlotFilter(True, True, True, True, True, True)
        self.selection_filter = SelectionFilter(True, True, True)

        self.create_axes()
        self.create_scale_bar()
        self.create_logos()
        self.set_theme("light")

    def update_plot(self, reset_camera=True):
        self.remove_actors()
        self.create_logos()

        project = app().project

        self.nodes_actor = NodesActor(project)
        self.lines_actor = ElementLinesActor(project)
        self.tubes_actor = TubeActor(project)

        # TODO: Replace these actors for newer ones that
        # are lighter and easier to update
        self._acoustic_nodes_symbols = AcousticNodesSymbolsActor(project)
        self._acoustic_elements_symbols = AcousticElementsSymbolsActor(project)
        self._structural_nodes_symbols = StructuralNodesSymbolsActor(project)
        self._structural_elements_symbols = StructuralElementsSymbolsActor(project)
        self._acoustic_nodes_symbols.build()
        self._acoustic_elements_symbols.build()
        self._structural_nodes_symbols.build()
        self._structural_elements_symbols.build()
        self.acoustic_nodes_symbols_actor = self._acoustic_nodes_symbols.getActor()
        self.acoustic_elements_symbols_actor = self._acoustic_elements_symbols.getActor()
        self.structural_nodes_symbols_actor = self._structural_nodes_symbols.getActor()
        self.structural_elements_symbols_actor = self._structural_elements_symbols.getActor()

        self.renderer.AddActor(self.lines_actor)
        self.renderer.AddActor(self.nodes_actor)
        self.renderer.AddActor(self.tubes_actor)
        self.renderer.AddActor(self.acoustic_nodes_symbols_actor)
        self.renderer.AddActor(self.acoustic_elements_symbols_actor)
        self.renderer.AddActor(self.structural_nodes_symbols_actor)
        self.renderer.AddActor(self.structural_elements_symbols_actor)

        if reset_camera:
            self.renderer.ResetCamera()
        # self.update()

    def remove_actors(self):
        self.renderer.RemoveActor(self.lines_actor)
        self.renderer.RemoveActor(self.nodes_actor)
        self.renderer.RemoveActor(self.tubes_actor)
        self.renderer.RemoveActor(self.acoustic_nodes_symbols_actor)
        self.renderer.RemoveActor(self.acoustic_elements_symbols_actor)
        self.renderer.RemoveActor(self.structural_nodes_symbols_actor)
        self.renderer.RemoveActor(self.structural_elements_symbols_actor)

        self.nodes_actor = None
        self.lines_actor = None
        self.tubes_actor = None
        self.acoustic_nodes_symbols_actor = None
        self.acoustic_elements_symbols_actor = None
        self.structural_nodes_symbols_actor = None
        self.structural_elements_symbols_actor = None

    def update_visualization(self, nodes, lines, tubes, symbols):
        transparent = nodes or lines or symbols
        self.plot_filter = PlotFilter(
            nodes=nodes,
            lines=lines,
            tubes=tubes,
            acoustic_symbols=symbols,
            structural_symbols=symbols,
            transparent=transparent,
        )
        
        elements = (lines or tubes) and nodes
        entities = (lines or tubes) and (not nodes) 
        self.selection_filter = SelectionFilter(
            nodes=nodes,
            elements=elements,
            entities=entities,
        )

        if not self._actor_exists():
            return 

        self.nodes_actor.SetVisibility(self.plot_filter.nodes)
        self.lines_actor.SetVisibility(self.plot_filter.lines)
        self.tubes_actor.SetVisibility(self.plot_filter.tubes)
        self.acoustic_nodes_symbols_actor.SetVisibility(self.plot_filter.acoustic_symbols)
        self.acoustic_elements_symbols_actor.SetVisibility(self.plot_filter.acoustic_symbols)
        self.structural_nodes_symbols_actor.SetVisibility(self.plot_filter.structural_symbols)
        self.structural_elements_symbols_actor.SetVisibility(self.plot_filter.structural_symbols)
        self.update()

    def _actor_exists(self):
        actors = [
            self.nodes_actor,
            self.lines_actor,
            self.tubes_actor,
            self.acoustic_nodes_symbols_actor,
            self.acoustic_elements_symbols_actor,
            self.structural_nodes_symbols_actor,
            self.structural_elements_symbols_actor,
        ]
        return all([actor is not None for actor in actors])

    def set_theme(self, theme):
        super().set_theme(theme)
        try:
            self.create_logos(theme)
        except:
            return

    def create_logos(self, theme="light"):
        self.renderer.RemoveViewProp(self.open_pulse_logo)
        self.renderer.RemoveViewProp(self.mopt_logo)
        self.renderer.AddViewProp(self.open_pulse_logo)
        self.renderer.AddViewProp(self.mopt_logo)

        if theme == "light":
            open_pulse_path = Path('data/icons/OpenPulse_logo_black.png')
            mopt_path = Path('data/icons/mopt_logo_black.png')     
        elif theme == "dark":
            open_pulse_path = Path('data/icons/OpenPulse_logo_white.png')
            mopt_path = Path('data/icons/mopt_logo_white.png')
        else:
            raise NotImplementedError()

        self.open_pulse_logo = self._load_vtk_logo(open_pulse_path)
        self.open_pulse_logo.SetPosition(0.845, 0.89)
        self.open_pulse_logo.SetPosition2(0.15, 0.15)
        self.renderer.AddViewProp(self.open_pulse_logo)
        self.open_pulse_logo.SetRenderer(self.renderer)

        self.mopt_logo = self._load_vtk_logo(mopt_path)
        self.mopt_logo.SetPosition(0.01, -0.015)
        self.mopt_logo.SetPosition2(0.07, 0.1)
        self.renderer.AddViewProp(self.mopt_logo)
        self.mopt_logo.SetRenderer(self.renderer)

    def _load_vtk_logo(self, path):
        image_reader = vtk.vtkPNGReader()
        image_reader.SetFileName(path)
        image_reader.Update()

        logo = vtk.vtkLogoRepresentation()
        logo.SetImage(image_reader.GetOutput())
        logo.ProportionalResizeOn()
        logo.GetImageProperty().SetOpacity(0.9)
        logo.GetImageProperty().SetDisplayLocationToBackground()
        return logo

    def click_callback(self, x, y):
        self.mouse_click = x, y

    def selection_callback(self, x, y):
        if not self._actor_exists():
            return 

        picked_nodes = self._pick_nodes(x, y)
        picked_entities = self._pick_property(x, y, "entity_index", self.tubes_actor)
        picked_elements = self._pick_property(x, y, "element_index", self.lines_actor)

        # selection priority is: nodes > elements > entities
        if len(picked_nodes) == 1 and len(picked_entities) <= 1 and len(picked_elements) <= 1:
            picked_entities.clear()
            picked_elements.clear()
        elif len(picked_elements) == 1 and len(picked_entities) <= 1:
            picked_entities.clear()

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = bool(modifiers & Qt.ControlModifier)
        shift_pressed = bool(modifiers & Qt.ShiftModifier)
        alt_pressed = bool(modifiers & Qt.AltModifier)

        self.update_selection_info(picked_nodes, picked_elements, picked_entities)
        
        self.nodes_actor.clear_colors()
        self.lines_actor.clear_colors()
        self.tubes_actor.clear_colors()

        selection_color = (255, 0, 0)
        self.nodes_actor.set_color(selection_color, picked_nodes)
        self.lines_actor.set_color(selection_color, elements=picked_elements)
        self.tubes_actor.set_color(selection_color, elements=picked_elements, entities=picked_entities)

    def _pick_nodes(self, x, y):
        picked = self._pick_actor(x, y, self.nodes_actor)
        if not self.nodes_actor in picked:
            return set()

        cells = picked[self.nodes_actor]
        return set(cells)
    
    def _pick_actor(self, x, y, actor_to_select):
        selection_picker = CellAreaPicker()
        selection_picker._cell_picker.SetTolerance(0.0015)
        pickability = dict()

        for actor in self.renderer.GetActors():
            pickability[actor] = actor.GetPickable()
            if actor == actor_to_select:
                actor.PickableOn()
            else:
                actor.PickableOff()

        x0, y0 = self.mouse_click
        mouse_moved = (abs(x0 - x) > 10) or (abs(y0 - y) > 10)
        if mouse_moved:
            selection_picker.area_pick(x0, y0, x, y, self.renderer)
        else:
            selection_picker.pick(x, y, 0, self.renderer)

        for actor in self.renderer.GetActors():
            actor.SetPickable(pickability[actor])

        return selection_picker.get_picked()

    def _pick_property(self, x, y, property_name, desired_actor):
        selection_picker = CellPropertyAreaPicker(property_name, desired_actor)
        selection_picker._cell_picker.SetTolerance(0.0015)
        pickability = dict()

        for actor in self.renderer.GetActors():
            pickability[actor] = actor.GetPickable()
            if actor == desired_actor:
                actor.PickableOn()
            else:
                actor.PickableOff()

        x0, y0 = self.mouse_click
        mouse_moved = (abs(x0 - x) > 10) or (abs(y0 - y) > 10)
        if mouse_moved:
            selection_picker.area_pick(x0, y0, x, y, self.renderer)
        else:
            selection_picker.pick(x, y, 0, self.renderer)

        for actor in self.renderer.GetActors():
            actor.SetPickable(pickability[actor])

        return selection_picker.get_picked()

    def update_selection_info(self, nodes, elements, entities):
        info_text = ""
        info_text += self._nodes_info_text(nodes)
        info_text += self._elements_info_text(elements)
        info_text += self._entity_info_text(entities)
        self.set_info_text(info_text)

    def _nodes_info_text(self, nodes):
        info_text = ""
        if len(nodes) > 1:
            info_text += (
                f"{len(nodes)} NODES IN SELECTION\n"
                f"{format_long_sequence(nodes)}\n\n"
            )
        return info_text

    def _elements_info_text(self, elements):
        info_text = ""
        project = app().project

        if len(elements) == 1:
            _id, *_ = elements
            structural_element = project.get_structural_element(_id)
            acoustic_element = project.get_acoustic_element(_id)

            first_node = structural_element.first_node
            last_node = structural_element.last_node

            tree = TreeInfo(f"ELEMENT {_id}")
            tree.add_item(f"First Node - {first_node.external_index:>5}",
                          "({:.3f}, {:.3f}, {:.3f})".format(*first_node.coordinates),
                          "m")
            tree.add_item(f"Last Node  - {last_node.external_index:>5}",
                          "({:.3f}, {:.3f}, {:.3f})".format(*last_node.coordinates),
                          "m")
            info_text += str(tree)

            if structural_element.material:
                info_text += self._material_info_text(structural_element.material)

            if acoustic_element.fluid:
                info_text += self._fluid_info_text(acoustic_element.fluid)

            info_text += self._cross_section_info_text(
                structural_element.cross_section, structural_element.element_type)

        elif len(elements) > 1:
            info_text += (
                f"{len(elements)} ELEMENTS IN SELECTION\n"
                f"{format_long_sequence(elements)}\n\n"
            )
        return info_text

    def _entity_info_text(self, entities):
        info_text = ""
        project = app().project

        if len(entities) == 1:
            _id, *_ = entities
            entity = project.get_entity(_id)

            info_text += f"LINE {_id}\n\n"

            if entity.material:
                info_text += self._material_info_text(entity.material)

            if entity.fluid:
                info_text += self._fluid_info_text(entity.fluid)

            info_text += self._cross_section_info_text(entity.cross_section, entity.structural_element_type)

        elif len(entities) > 1:
            info_text += (
                f"{len(entities)} LINES IN SELECTION\n"
                f"{format_long_sequence(entities)}\n\n"
            )

        return info_text
    
    def _material_info_text(self, material):
        tree = TreeInfo("Material")
        tree.add_item("Name", material.name)
        return str(tree)

    def _fluid_info_text(self, fluid):
        tree = TreeInfo("fluid")
        tree.add_item("Name", fluid.name)
        if fluid.temperature:
            tree.add_item("Temperature", round(fluid.temperature, 4), "K")
        if fluid.pressure:
            tree.add_item("Pressure", round(fluid.pressure, 4), "Pa")
        return str(tree)

    def _cross_section_info_text(self, cross_section, element_type):
        info_text = ""

        if cross_section is None:
            tree = TreeInfo("cross section")
            tree.add_item("Info", "Undefined")
            info_text += str(tree)

        elif element_type == 'beam_1':
            tree = TreeInfo("cross section")
            tree.add_item("Area", round(cross_section.area, 2), "m²")
            tree.add_item("Iyy", round(cross_section.second_moment_area_y, 4), "m⁴")
            tree.add_item("Izz", round(cross_section.second_moment_area_z, 4), "m⁴")
            tree.add_item("Iyz", round(cross_section.second_moment_area_yz, 4), "m⁴")
            tree.add_item("x-axis rotation", round(cross_section.second_moment_area_yz, 4), "m⁴")
            info_text += str(tree)

        elif element_type in ['pipe_1', 'valve']:
            tree = TreeInfo("cross section")
            tree.add_item("Outer Diameter", round(cross_section.outer_diameter, 4), "m")
            tree.add_item("Thickness", round(cross_section.thickness, 4), "m")
            tree.add_separator()
            if cross_section.offset_y or cross_section.offset_z:
                tree.add_item("Offset Y", round(cross_section.offset_y, 4), "m")
                tree.add_item("Offset Z", round(cross_section.offset_z, 4), "m")
                tree.add_separator()
            if cross_section.insulation_thickness or cross_section.insulation_density:
                tree.add_item("Insulation Thickness", round(cross_section.insulation_thickness, 4), "m")
                tree.add_item("Insulation Density", round(cross_section.insulation_density, 4), "kg/m³")
            info_text += str(tree)
        
        return info_text
