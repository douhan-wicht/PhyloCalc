# PhyloCalc [WORK IN PROGRESS]

## Introduction
PhyloCalc is a custom Python module designed to calculate the probability of a phylogenetic tree, accounting for varying nucleotide substitution probabilities. Developed for the Advanced Python Programming Course in the University of Lausanne’s first-year Master of Molecular Life Sciences program, PhyloCalc operates independently of the Biopython library.

## Key Features
- **Phylogenetic Tree Probability Calculation**: PhyloCalc computes the likelihood of a phylogenetic tree based on given DNA sequences, tree structure, and branch lengths. It also predicts the most probable nucleotide mutation rates.
- **FASTA File Integration**: The module supports FASTA file input, allowing users to seamlessly incorporate their DNA sequence data.
- **Tree Structure Parsing**: PhyloCalc can interpret tree structures in tabular format, facilitating compatibility with various tree representations.
- **Visualization**: PhyloCalc can generate visualizations of phylogenetic trees, providing a clearer view of evolutionary relationships.

## Friday 09.11.2024 - Preliminary Step: Overview of the Project

```mermaid
flowchart TD
    A[Input Tree Table] --> B{Parse Data}
    A2[Input Branch Length Vector] --> B
    A3[FASTA File with Sequences] --> C[Generate Possible Sequence Attributions]

    B --> D[Create Tree Class with Tree Structure]
    D --> E[Iterate Over Possible Sequence Attributions]

    E --> F{Populate Tree Using Node Class}
    F --> F1[Assign Node Identity]
    F --> F2[Assign Parent Attribute]
    F --> F3[Assign Children Attribute]
    F --> F4[Assign Branch Length to Closest Parent]
    
    F --> G{Assign Sequence}
    G --> G1[Assign Sequence from FASTA to Final Nodes]
    G --> G2[Calculate Ancestral Sequence for Parent Nodes]
    
    G2 --> H[Populated Tree Structure with Sequence Alignment]
    H --> I[Calculate Probability of Alignment]
    I --> E

    I --> J{Evaluate All Alignments}
    J --> K[Output Most Probable Tree]
```
