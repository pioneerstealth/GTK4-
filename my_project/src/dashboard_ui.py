import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk

class DashboardWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Robot Probe Dashboard")
        self.set_default_size(1200, 800)

        # Store references to updateable widgets
        self.updateable_widgets = {}

        # Main layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_child(main_box)

        # Left panel (Test Scenario Configuration)
        left_panel = self.create_left_panel()
        main_box.append(left_panel)

        # Main content area
        content_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.append(content_area)

        # Top bar (Dashboard Overview)
        top_bar = self.create_top_bar()
        content_area.append(top_bar)

        # Center area (Main Panel and Probe Control)
        center_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        content_area.append(center_area)

        # Main panel
        main_panel = self.create_main_panel()
        center_area.append(main_panel)

        # Right panel (Probe Control and ML Vision)
        right_panel = self.create_right_panel()
        center_area.append(right_panel)

        # Bottom area (Feedback Collection & Reporting)
        bottom_area = self.create_bottom_area()
        content_area.append(bottom_area)

        # Apply CSS styling
        self.apply_css()

    def create_left_panel(self):
        left_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        left_panel.set_size_request(250, -1)
        left_panel.add_css_class("left-panel")

        scenarios_label = Gtk.Label(label="Test Scenarios")
        scenarios_label.add_css_class("panel-title")
        left_panel.append(scenarios_label)

        scenarios_list = Gtk.ListBox()
        scenarios_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        left_panel.append(scenarios_list)

        for scenario in ["Scenario 1", "Scenario 2", "Scenario 3"]:
            row = Gtk.ListBoxRow()
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            label = Gtk.Label(label=scenario)
            box.append(label)
            row.set_child(box)
            scenarios_list.append(row)

        custom_input_label = Gtk.Label(label="Custom Input")
        custom_input_label.add_css_class("panel-title")
        left_panel.append(custom_input_label)

        custom_input = Gtk.Entry()
        custom_input.set_placeholder_text("Enter custom parameters")
        left_panel.append(custom_input)

        return left_panel

    def create_top_bar(self):
        top_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        top_bar.add_css_class("top-bar")

        coordinates_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        coordinates_box.add_css_class("coordinates-box")
        for coord in ['X', 'Y', 'Z']:
            label = Gtk.Label(label=f"{coord}: 0.00")
            label.add_css_class("coordinate-label")
            coordinates_box.append(label)
            self.updateable_widgets[f"{coord.lower()}_coordinate_label"] = label
        top_bar.append(coordinates_box)

        for action in ["Start Test", "Stop Test", "Pause Test"]:
            button = Gtk.Button(label=action)
            button.add_css_class("action-button")
            top_bar.append(button)
            self.updateable_widgets[f"{action.lower().replace(' ', '_')}_button"] = button

        return top_bar

    def create_main_panel(self):
        main_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_panel.set_size_request(600, -1)
        main_panel.add_css_class("main-panel")

        # Placeholder for camera feed
        camera_feed = Gtk.DrawingArea()
        camera_feed.set_size_request(400, 300)
        camera_feed.add_css_class("camera-feed")
        main_panel.append(camera_feed)

        return main_panel

    def create_right_panel(self):
        right_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        right_panel.set_size_request(250, -1)
        right_panel.add_css_class("right-panel")

        # Probe Control Interface
        probe_control_label = Gtk.Label(label="Probe Control")
        probe_control_label.add_css_class("panel-title")
        right_panel.append(probe_control_label)

        control_grid = Gtk.Grid()
        control_grid.set_row_spacing(5)
        control_grid.set_column_spacing(5)
        right_panel.append(control_grid)

        for i, direction in enumerate(['Up', 'Left', 'Right', 'Down']):
            button = Gtk.Button(label=direction)
            button.add_css_class("direction-button")
            row = i // 3
            col = i % 3
            if direction == 'Up':
                control_grid.attach(button, 1, 0, 1, 1)
            elif direction == 'Down':
                control_grid.attach(button, 1, 2, 1, 1)
            else:
                control_grid.attach(button, col, 1, 1, 1)

        # ML Vision System
        ml_vision_label = Gtk.Label(label="ML Vision System")
        ml_vision_label.add_css_class("panel-title")
        right_panel.append(ml_vision_label)

        recognition_label = Gtk.Label(label="Recognition: None")
        recognition_label.add_css_class("recognition-label")
        right_panel.append(recognition_label)
        self.updateable_widgets["recognition_label"] = recognition_label

        upload_button = Gtk.Button(label="Upload Training Data")
        upload_button.add_css_class("upload-button")
        right_panel.append(upload_button)

        return right_panel

    def create_bottom_area(self):
        bottom_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        bottom_area.add_css_class("bottom-area")

        results_label = Gtk.Label(label="Test Results")
        results_label.add_css_class("panel-title")
        bottom_area.append(results_label)

        # Create a simple list store as a placeholder for the results table
        list_store = Gtk.ListStore(str, str, str, str)
        list_store.append(["Scenario 1", "Pass", "2024-03-20 10:30", "Details..."])
        list_store.append(["Scenario 2", "Fail", "2024-03-20 11:45", "Details..."])

        tree_view = Gtk.TreeView(model=list_store)
        for i, column_title in enumerate(["Test Scenario", "Result", "Timestamp", "Details"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            tree_view.append_column(column)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_child(tree_view)
        scrolled_window.set_size_request(-1, 150)
        bottom_area.append(scrolled_window)

        return bottom_area

    def apply_css(self):
        css_provider = Gtk.CssProvider()
        css = """
        .left-panel, .right-panel { background-color: #f0f0f0; padding: 10px; }
        .main-panel { background-color: #ffffff; padding: 10px; }
        .top-bar { background-color: #e0e0e0; padding: 10px; }
        .bottom-area { background-color: #f5f5f5; padding: 10px; }
        .panel-title { font-weight: bold; font-size: 16px; margin-bottom: 10px; }
        .coordinate-label { font-family: monospace; }
        .action-button { background-color: #4CAF50; color: white; padding: 5px 10px; }
        .direction-button { padding: 5px 10px; }
        .camera-feed { background-color: #000000; }
        .recognition-label { font-style: italic; }
        .upload-button { background-color: #2196F3; color: white; padding: 5px 10px; }
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def get_updateable_widget(self, widget_name):
        return self.updateable_widgets.get(widget_name)

class DashboardApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.Dashboard")

    def do_activate(self):
        win = DashboardWindow(self)
        win.present()