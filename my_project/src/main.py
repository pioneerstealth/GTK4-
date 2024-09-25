from dashboard_ui import DashboardWindow, DashboardApp
from dashboard_control import DashboardControl

class MyDashboardApp(DashboardApp):
    def do_activate(self):
        win = DashboardWindow(self)
        control = DashboardControl(win)
        win.present()

app = MyDashboardApp()
app.run(None)