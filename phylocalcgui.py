import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QPushButton, QLabel, QFileDialog, QDoubleSpinBox,
                             QMessageBox, QTableWidget, QTableWidgetItem)
from tree_visualization import TreeVisualization  # Import the tree visualization popup class
import numpy as np


class PhyloCalcGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhyloCalc GUI")
        self.setGeometry(100, 100, 600, 600)

        self.table_file = None
        self.msa_file = None
        self.branch_file = None
        self.Q_matrix = np.zeros((4, 4))

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        self.add_file_buttons()
        self.add_matrix_editor()
        self.add_matrix_display()
        self.add_run_section()
        self.add_tree_viewer_button()

    def add_file_buttons(self):
        self.table_btn = QPushButton("Load Table File")
        self.table_btn.clicked.connect(lambda: self.load_file('table'))
        self.layout.addWidget(self.table_btn)

        self.msa_btn = QPushButton("Load MSA File")
        self.msa_btn.clicked.connect(lambda: self.load_file('msa'))
        self.layout.addWidget(self.msa_btn)

        self.branch_btn = QPushButton("Load Branch Length File")
        self.branch_btn.clicked.connect(lambda: self.load_file('branch'))
        self.layout.addWidget(self.branch_btn)

        self.table_path_display = QLabel("Table File: Not Loaded")
        self.layout.addWidget(self.table_path_display)

        self.msa_path_display = QLabel("MSA File: Not Loaded")
        self.layout.addWidget(self.msa_path_display)

        self.branch_path_display = QLabel("Branch Length File: Not Loaded")
        self.layout.addWidget(self.branch_path_display)

    def load_file(self, file_type):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, f"Open {file_type} file", "", "Data Files (*.dat *.csv)")

        if file_path:
            if file_type == 'table':
                self.table_file = file_path
                self.table_path_display.setText(f"Table File: {file_path}")
            elif file_type == 'msa':
                self.msa_file = file_path
                self.msa_path_display.setText(f"MSA File: {file_path}")
            elif file_type == 'branch':
                self.branch_file = file_path
                self.branch_path_display.setText(f"Branch Length File: {file_path}")

    def add_matrix_editor(self):
        self.layout.addWidget(QLabel("Set value for µ in Q Matrix:"))

        self.x_input = QDoubleSpinBox()
        self.x_input.setRange(0.0, 10.0)
        self.x_input.setDecimals(4)
        self.x_input.setSingleStep(0.01)
        self.x_input.setValue(0.1875)
        self.x_input.valueChanged.connect(self.update_Q_matrix)

        self.layout.addWidget(self.x_input)

    def add_matrix_display(self):
        self.matrix_display_label = QLabel("Q Matrix:")
        self.layout.addWidget(self.matrix_display_label)

        self.q_table = QTableWidget(4, 4)
        self.q_table.setHorizontalHeaderLabels(["A", "C", "G", "T"])
        self.q_table.setVerticalHeaderLabels(["A", "C", "G", "T"])
        self.q_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Make the table non-editable
        self.layout.addWidget(self.q_table)

        self.update_Q_matrix()

    def update_Q_matrix(self):
        # Update the matrix based on x
        x = self.x_input.value()
        self.Q_matrix = np.array([
            [-3 * x, x, x, x],
            [x, -3 * x, x, x],
            [x, x, -3 * x, x],
            [x, x, x, -3 * x]
        ])

        # Update the Q table with the new matrix values
        for i in range(4):
            for j in range(4):
                self.q_table.setItem(i, j, QTableWidgetItem(f"{self.Q_matrix[i, j]:.4f}"))

    def add_run_section(self):
        self.run_btn = QPushButton("Run Phylogenetic Calculation")
        self.run_btn.clicked.connect(self.run_calculation)
        self.layout.addWidget(self.run_btn)

        self.runtime_display = QLabel("Runtime: Not calculated")
        self.layout.addWidget(self.runtime_display)

        self.log_likelihood_display = QLabel("Log Likelihood: Not calculated")
        self.layout.addWidget(self.log_likelihood_display)

    def run_calculation(self):
        if not all([self.table_file, self.msa_file, self.branch_file]):
            QMessageBox.warning(self, "Missing Files", "Please load all data files before running the calculation.")
            return

        start_time = time.time()

        try:
            # Simulating some calculation
            time.sleep(1)  # Simulated delay
            log_likelihood = -123.456  # Example log likelihood
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during calculation: {e}")
            return

        runtime = time.time() - start_time
        self.runtime_display.setText(f"Runtime: {runtime:.4f} seconds")
        self.log_likelihood_display.setText(f"Log Likelihood: {log_likelihood:.4f}")

    def add_tree_viewer_button(self):
        self.tree_viewer_btn = QPushButton("View Phylogenetic Tree")
        self.tree_viewer_btn.clicked.connect(self.show_tree_viewer)
        self.layout.addWidget(self.tree_viewer_btn)

    def show_tree_viewer(self):
        tree_viewer = TreeVisualization(self)
        tree_viewer.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = PhyloCalcGUI()
    gui.show()
    sys.exit(app.exec())
