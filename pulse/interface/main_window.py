from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QSplitter, QStackedWidget, QLabel, QToolBar, QComboBox, QSizePolicy
from PyQt5 import uic
from pathlib import Path

from pulse import app
from pulse.interface.viewer_3d.render_widgets import MeshRenderWidget
from pulse.uix.menu.Menu import Menu
from pulse.uix.input_ui import InputUi
from pulse.uix.opv_ui import OPVUi

from data.user_input.model.geometry.geometry_designer import OPPGeometryDesignerInput

from opps.interface.viewer_3d.render_widgets.editor_render_widget import EditorRenderWidget


UI_DIR = Path('pulse/interface/ui_files/')


class MainWindow(QMainWindow):
    permission_changed = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(UI_DIR / 'main_window.ui', self)

        # i am keeping these atributes here to make
        # the transition easier, but it should be
        # defined only in the app.
        self.config = app().config
        self.project = app().project
        self.input_widget = InputUi(app().project, self)

        self._config_window()
        self._define_qt_variables()
        self._connect_actions()
        self._create_layout()
        self._create_workspaces_toolbar()
        self._update_recent_projects()

        self.use_geometry_workspace()

    # public
    def use_geometry_workspace(self):
        self.setup_widgets_stack.setCurrentWidget(self.geometry_input_wigdet)
        self.render_widgets_stack.setCurrentWidget(self.geometry_widget)

    def use_mesh_workspace(self):
        self.setup_widgets_stack.setCurrentWidget(self.menu_widget)
        self.render_widgets_stack.setCurrentWidget(self.opv_widget)
        # self.setup_widgets_stack.setCurrentWidget(self.mesh_input_wigdet)
        # self.render_widgets_stack.setCurrentWidget(self.mesh_widget)

    def use_results_workspace(self):
        self.setup_widgets_stack.setCurrentWidget(self.results_input_wigdet)
        self.render_widgets_stack.setCurrentWidget(self.results_widget)  

    def set_window_title(self, msg=""):
        title = "OpenPulse"
        if (msg != ""):
            title += " - " + msg
        self.setWindowTitle(title)

    def show_get_started_window(self):
        config = app().config

        if config.openLastProject and config.haveRecentProjects():
            self.load_project(config.getMostRecentProjectDir())
        else:
            if self.inputWidget.getStarted(config):
                self._loadProjectMenu()
                self.changeWindowTitle(self.project.file._project_name)
                # self.draw()

    def load_project(self, path=None):
        if self.input_widget.loadProject(app().config, path):
            self.set_window_title(self.project.file._project_name)
            # self.draw()

    # internal
    def _update_recent_projects(self):
        actions = self.menurecent.actions()
        for action in actions:
            self.menurecent.removeAction(action)

        self.menu_actions = []
        for name, path in self.config.recentProjects.items():
            import_action = QAction(str(name) + "\t" + str(path))
            import_action.setStatusTip(str(path))
            import_action.triggered.connect(lambda: self.load_project(path))
            self.menurecent.addAction(import_action)
            self.menu_actions.append(import_action)

    def _config_window(self):
        self.showMaximized()
        self.installEventFilter(self)
    
    def _define_qt_variables(self):
        '''
        This function is doing nothing. Every variable was
        already defined in the UI file.

        Despite that, it is nice to list the variables to
        future maintainers and to help the code editor with
        type inference.
        '''
        self.setup_widgets_stack: QStackedWidget
        self.render_widgets_stack: QStackedWidget
        self.action_geometry_workspace: QAction
        self.action_mesh_workspace: QAction
        self.action_results_workspace: QAction
        self.tool_bar: QToolBar
        self.splitter: QSplitter
        self.menurecent: QMenu

    def _connect_actions(self):
        '''
        Instead of connecting every action manually, one by one,
        this function loops through every action and connects it
        to a function ending with "_callback".

        For example an action named "action_new" will be connected to 
        the function named "action_new_callback" if it exists.
        '''
        for action in self.findChildren(QAction):
            function_name = action.objectName() + "_callback"
            function_exists = hasattr(self, function_name)
            if not function_exists:
                continue

            function = getattr(self, function_name)
            if callable(function):
                action.triggered.connect(function)

    def _create_workspaces_toolbar(self):
        actions = [
            self.action_geometry_workspace,
            self.action_mesh_workspace,
            self.action_results_workspace
        ]
        combo_box = QComboBox()
        for action in actions:
            action: QAction 
            combo_box.addItem(action.text())
        combo_box.currentIndexChanged.connect(lambda x: actions[x].trigger())
        self.tool_bar.addWidget(combo_box)

    def _create_layout(self):
        editor = app().geometry_toolbox.editor

        self.menu_widget = Menu(self)
        self.opv_widget = OPVUi(self.project, self)
        self.opv_widget.opvAnalysisRenderer._createPlayer()
        self.opv_widget.updatePlots()
        self.opv_widget.changePlotToEntitiesWithCrossSection()

        self.mesh_widget = MeshRenderWidget()
        self.geometry_widget = EditorRenderWidget(editor)
        self.results_widget = QLabel("RESULTS")
        self.render_widgets_stack.addWidget(self.mesh_widget)
        self.render_widgets_stack.addWidget(self.geometry_widget)
        self.render_widgets_stack.addWidget(self.results_widget)
        self.render_widgets_stack.addWidget(self.opv_widget)

        self.geometry_input_wigdet = OPPGeometryDesignerInput(self.geometry_widget)
        self.mesh_input_wigdet = QLabel("mesh")
        self.results_input_wigdet = QLabel("results")
        self.setup_widgets_stack.addWidget(self.geometry_input_wigdet)
        self.setup_widgets_stack.addWidget(self.mesh_input_wigdet)
        self.setup_widgets_stack.addWidget(self.results_input_wigdet)
        self.setup_widgets_stack.addWidget(self.menu_widget)

        self.splitter.setSizes([120, 400])

    # callbacks
    def action_geometry_workspace_callback(self):
        self.use_geometry_workspace()

    def action_mesh_workspace_callback(self):
        self.use_mesh_workspace()

    def action_results_workspace_callback(self):
        self.use_results_workspace()
