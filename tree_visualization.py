from PyQt6.QtWidgets import QDialog, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import networkx as nx

class TreeVisualization(QDialog):
    def __init__(self, tree, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Phylogenetic Tree Viewer")
        self.setGeometry(200, 200, 800, 600)

        self.tree = tree  # Store the Tree object passed from PhyloCalcGUI

        layout = QVBoxLayout(self)
        self.canvas = FigureCanvas(plt.figure(figsize=(8, 6)))
        layout.addWidget(self.canvas)
        self.plot_tree()

    def plot_tree(self):
        # Build the phylogenetic tree dynamically
        graph = nx.DiGraph()

        # Add nodes and edges based on the tree structure
        for node_name, node in self.tree.nodes.items():
            if node.parent:
                graph.add_edge(node.parent.name, node_name, length=node.branch_length)

        # Assign positions for a hierarchical tree
        pos = nx.drawing.nx_agraph.graphviz_layout(graph, prog="dot")

        # Draw the tree
        ax = self.canvas.figure.add_subplot(111)
        ax.clear()
        nx.draw(graph, pos, with_labels=True, node_size=500, node_color="lightblue", ax=ax)
        edge_labels = nx.get_edge_attributes(graph, "length")
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)
        ax.set_title("Phylogenetic Tree")
        self.canvas.draw()
