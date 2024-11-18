from PyQt6.QtWidgets import QDialog, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import networkx as nx


class TreeVisualization(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Phylogenetic Tree Viewer")
        self.setGeometry(200, 200, 800, 600)

        # Set up layout
        layout = QVBoxLayout(self)

        # Add Matplotlib canvas
        self.canvas = FigureCanvas(plt.figure(figsize=(8, 6)))
        layout.addWidget(self.canvas)

        # Draw the tree
        self.plot_tree()

    def plot_tree(self):
        # Define the phylogenetic tree with branch lengths
        tree = nx.DiGraph()
        tree.add_edge("6", "7", length=0.12)
        tree.add_edge("6", "8", length=0.14)
        tree.add_edge("7", "4", length=0.20)
        tree.add_edge("7", "5", length=0.08)
        tree.add_edge("8", "9", length=0.01)
        tree.add_edge("8", "3", length=0.04)
        tree.add_edge("9", "1", length=0.10)
        tree.add_edge("9", "2", length=0.40)

        # Assign positions for a hierarchical tree
        pos = nx.drawing.nx_agraph.graphviz_layout(tree, prog="dot")

        # Draw the tree
        ax = self.canvas.figure.add_subplot(111)
        ax.clear()
        nx.draw(tree, pos, with_labels=True, node_size=500, node_color="lightblue", ax=ax)
        edge_labels = nx.get_edge_attributes(tree, "length")
        nx.draw_networkx_edge_labels(tree, pos, edge_labels=edge_labels, ax=ax)
        ax.set_title("Phylogenetic Tree")
        self.canvas.draw()
