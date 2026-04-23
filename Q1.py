import sys
import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from scipy.integrate import quad

class TakeoffModel:
    def __init__(self):
        self.weight = 56000
        self.thrust = 13000
        self.S = 1000
        self.CLmax = 2.4
        self.rho = .002377
        self.CD = .0279
        self.gc = 32.2 #[ft/s^2]

    def calculate_Sto(self, thrust, weight):
        """Finds the take off distance using the 5 eqn's"""
        V_stall = np.sqrt(weight/((self.rho*self.S*self.CLmax)/2))
        V_TO = 1.2*V_stall
        A = self.gc*(thrust/weight)
        B=(self.gc/weight)*((self.rho*self.S*self.CD)/2)
        def integrand(v):
            return v/(A-B*(v**2))
        Sto, _ = quad(integrand, 0, V_TO)
        return Sto

class TakeoffView(qtw.QWidget):     #Outline written by Gemini AI
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Takeoff Distance Calculator")
        self.layout = qtw.QVBoxLayout(self)
        self.gb_input = qtw.QGroupBox("Aircraft Parameters")
        self.form_layout = qtw.QFormLayout(self.gb_input)
        self.le_weight = qtw.QLineEdit("56000")
        self.le_thrust = qtw.QLineEdit("13000")
        self.btn_calculate = qtw.QPushButton("Calculate S_TO")
        self.form_layout.addRow("Weight [lb]:", self.le_weight)
        self.form_layout.addRow("Thrust [lb]:", self.le_thrust)
        self.form_layout.addRow("", self.btn_calculate)
        self.layout.addWidget(self.gb_input)

        self.figure= Figure(figsize=(8,5), tight_layout=True)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

class TakeoffController:
    def __init__(self):
        self.model=TakeoffModel()
        self.view=TakeoffView()
        self.view.btn_calculate.clicked.connect(self.update_plot)
        self.update_plot()
    def update_plot(self):
        try:
            self.model.weight = float(self.view.le_weight.text())
            self.model.thrust = float(self.view.le_thrust.text())
        except ValueError:
            return

        self.view.ax.clear()
        thrust_vals = np.linspace(5000, 30000, 100)
        weights = [ #target range is W, W +/- 1000
            self.model.weight,
            self.model.weight - 10000,
            self.model.weight + 10000
        ]
        for w in weights:
            sto_vals = [self.model.calculate_Sto(t,w) for t in thrust_vals]
            self.view.ax.plot(thrust_vals, sto_vals, label=f"Weight = {w} lb")

            target_Sto = self.model.calculate_Sto(self.model.thrust, self.model.weight)
            self.view.ax.plot(self.model.thrust, target_Sto, 'ro', markersize=8, label = "Target S_TO")

            self.view.ax.set_xlabel("Thrust [lb]")
            self.view.ax.set_ylabel("Takeoff Distance, S_TO [ft]")
            self.view.ax.set_title("Takeoff Distance vs Engine Thrust")
            self.view.ax.grid(True)
            self.view.ax.legend()
            self.view.canvas.draw()

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    controller = TakeoffController()
    controller.view.show()
    sys.exit(app.exec_())
