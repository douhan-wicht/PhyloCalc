import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QPushButton, QLabel, QFileDialog, QTableWidget,
                             QTableWidgetItem, QMessageBox)
from phylocalc import Tree, Q


class PhyloCalcGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhyloCalc GUI")
        self.setGeometry(100, 100, 600, 400)

        self.table_file = None
        self.msa_file = None
        self.branch_file = None
        self.Q_matrix = Q.copy()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        self.add_file_buttons()
        self.add_matrix_editor()
        self.add_run_section()

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
        self.q_table = QTableWidget(4, 4)
        self.q_table.setHorizontalHeaderLabels(['A', 'C', 'G', 'T'])
        self.q_table.setVerticalHeaderLabels(['A', 'C', 'G', 'T'])

        for i in range(4):
            for j in range(4):
                item = QTableWidgetItem(str(self.Q_matrix[i, j]))
                self.q_table.setItem(i, j, item)

        self.layout.addWidget(QLabel("Edit Q Matrix:"))
        self.layout.addWidget(self.q_table)

    def update_Q_matrix(self):
        for i in range(4):
            for j in range(4):
                item = self.q_table.item(i, j)
                try:
                    self.Q_matrix[i, j] = float(item.text())
                except ValueError:
                    QMessageBox.warning(self, "Invalid Input", f"Invalid value in Q matrix at ({i}, {j}).")
                    return False
        return True

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

        if not self.update_Q_matrix():
            return

        start_time = time.time()

        try:
            tree = Tree(self.table_file, self.msa_file, self.branch_file, self.Q_matrix)
            log_likelihood = tree.get_log_likelihood()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during calculation: {e}")
            return

        runtime = time.time() - start_time
        self.runtime_display.setText(f"Runtime: {runtime:.4f} seconds")
        self.log_likelihood_display.setText(f"Log Likelihood: {log_likelihood:.4f}")

        tree.print_tree()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = PhyloCalcGUI()
    gui.show()
    sys.exit(app.exec())
