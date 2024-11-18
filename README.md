# PhyloCalc [WORK IN PROGRESS]

## Introduction
PhyloCalc is a custom Python module designed to calculate the probability of a phylogenetic tree, accounting for varying nucleotide substitution probabilities. Developed for the Advanced Python Programming Course in the University of Lausanne’s first-year Master of Molecular Life Sciences program, PhyloCalc operates independently of the Biopython library.

## Key Features
- **Phylogenetic Tree Probability Calculation**: PhyloCalc computes the likelihood of a phylogenetic tree based on given DNA sequences, tree structure, and branch lengths. ✅
- **Tree Structure Parsing**: PhyloCalc can interpret tree structures in tabular format, facilitating compatibility with various tree representations. ✅
- **Visualization**: PhyloCalc can generate visualizations of phylogenetic trees, providing a clearer view of evolutionary relationships. ✅

## Roadmap
- **FASTA File Integration**: The module supports FASTA file input, allowing users to seamlessly incorporate their DNA sequence data. [WIP] 🤔


## Friday 09.11.2024 - Preliminary Step: Overview of the Project

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

## Monday 11.11.2024 - Code Versioning

The algorithm responsible for creating the `Tree` object and calculating the log-likelihood is located in `phylocalc.py`. It can be accessed easily through the graphical interface by running the `phylocalcgui.py` script. Additionally, the method for visualizing the tree using NetworkX is implemented in `tree_visualization.py` and is imported into the GUI. If the required packages are installed, the tree will be displayed in a pop-up window for the user.
