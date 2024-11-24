# PhyloCalc [WORK IN PROGRESS]

## Overview
PhyloCalc is a Python module tailored to calculate the probability of phylogenetic trees, considering diverse nucleotide substitution probabilities. This tool was developed as part of the Advanced Python Programming Course at the University of Lausanne’s first-year Master of Molecular Life Sciences program. Importantly, PhyloCalc is designed to function independently of the `Biopython` library, ensuring a custom-built solution for specific phylogenetic analyses.

---

## Key Features
- **Phylogenetic Tree Likelihood Computation**  
  PhyloCalc calculates the likelihood of a phylogenetic tree based on DNA sequences, tree structures, and branch lengths. ✅  
- **Flexible Tree Parsing**  
  Reads tree structures in tabular formats, enhancing compatibility with different data representations. ✅  
- **Visual Representation**  
  Generates clear and intuitive visualizations of phylogenetic trees, aiding in the interpretation of evolutionary relationships. ✅  

### Upcoming Enhancements
- **FASTA File Integration**  
  Allowing direct input of DNA sequences from FASTA files to streamline the workflow. [Work in Progress] 🤔

---

## How It Works

### Workflow Diagram

```mermaid
flowchart TD
    A["Input Tree Table"] --> B{"Parse Data"}
    A2["Input Branch Length Vector"] --> B
    A3["FASTA File with Sequences"] --> B
    B --> D["Create Tree Class with Tree Structure"]
    D --> F{"Populate Tree Using Node Class"}
    F --> F1["Assign Node Identity"] & F2["Assign Parent Attribute"] & F3["Assign Children Attribute"] & F4["Assign Branch Length to Closest Parent"] & G{"Assign Sequence"}
    G --> G1["Assign Sequence from FASTA to Final Nodes"] & G2["Calculate Ancestral Sequence for Parent Nodes"]
    G2 --> H["Populated Tree Structure with Sequence Alignment"]
    H --> I["Calculate Probability of correct alignment for a given mutation rate"]
```
## Project Components

### Core Functionalities
1. **Tree Object Construction**  
   The core algorithm responsible for building the `Tree` object and calculating the log-likelihood is implemented in the `phylocalc.py` script.  
2. **Graphical Interface**  
   A user-friendly interface is provided via `phylocalcgui.py`. This script integrates all functionalities and allows users to interact with the module easily.  
3. **Tree Visualization**  
   Implemented in `tree_visualization.py`, the visualization functionality uses NetworkX to display the phylogenetic tree in a pop-up window (requires appropriate packages installed).  

---

## Installation and Setup

### Prerequisites
- Python 3.12 or higher
- Required packages:  
  ```bash
  pip install pyqt6 networkx numpy
  ```

### Get Started
1. **Clone the repository**
    ```bash
    git clone https://github.com/douhan-wicht/PhyloCalc
    cd PhyloCalc
    ```
2. **Run the GUI**
   ```bash
   python phylocalcgui.py
   ```

---

## Screenshots

<div style="display: flex; justify-content: space-between;">
![PhyloCalcGUI](ressources/PhyloCalcGUI.png)
![Tree Visualization Screenshot](ressources/tree_visualization.png)
</div>
