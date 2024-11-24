import pandas as pd
import numpy as np
from scipy.linalg import expm
import os
import tempfile

Q = np.array([[-0.9, 0.3, 0.3, 0.3],
              [0.3, -0.9, 0.3, 0.3],
              [0.3, 0.3, -0.9, 0.3],
              [0.3, 0.3, 0.3, -0.9]])


class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []
        self.branch_length = None
        self.sequence = None
        self.is_final = False


class Tree:
    def __init__(self, table_path, msa_path, branch_lengths_path, transition_matrix):
        # Preprocess files before using them
        table_path, msa_path, branch_lengths_path = self.preprocess_files_if_needed(
            table_path, msa_path, branch_lengths_path
        )

        self.data = self.get_data(table_path, msa_path, branch_lengths_path)
        self.root = None
        self.transition_matrix = transition_matrix
        self.populate_tree(self.data)
        self.tree_probability(self.root)

    @staticmethod
    def preprocess_files_if_needed(table_path, msa_path, branch_lengths_path):
        # Preprocess the table file
        tree_table = pd.read_csv(table_path, sep=',', header=None, names=['Parent', 'Child'])

        # Ensure MSA file has the correct structure
        msa = pd.read_csv(msa_path, sep=' ', header=None)
        if msa.shape[1] != 2:
            raise ValueError(f"MSA file must have two columns. Detected columns: {msa.shape[1]}")
        msa.columns = ['Species', 'Sequence']

        # Assign unique identifiers to species in the MSA
        species_to_id = {species: idx + 1 for idx, species in enumerate(msa['Species'])}
        msa['Species'] = msa['Species'].map(species_to_id)

        # Replace species names in the tree table
        def map_species_to_id(value):
            return species_to_id.get(value, value)  # Map species or leave internal nodes as-is

        tree_table['Child'] = tree_table['Child'].apply(map_species_to_id)
        tree_table['Parent'] = tree_table['Parent'].apply(map_species_to_id)

        # Ensure branch lengths have the correct structure
        branch_lengths = pd.read_csv(branch_lengths_path, sep=',', header=None)
        branch_lengths = branch_lengths.T
        if branch_lengths.shape[1] != 1:
            raise ValueError(f"Branch lengths file must have exactly one column. Detected columns: {branch_lengths.shape[1]}")

        # Save transformed files as temporary files
        temp_dir = tempfile.mkdtemp()
        transformed_table_path = os.path.join(temp_dir, 'transformed_table.csv')
        transformed_msa_path = os.path.join(temp_dir, 'transformed_msa.csv')
        transformed_branch_lengths_path = os.path.join(temp_dir, 'transformed_branch_lengths.csv')

        tree_table.to_csv(transformed_table_path, index=False, header=False)
        msa.to_csv(transformed_msa_path, index=False, header=False)
        branch_lengths.to_csv(transformed_branch_lengths_path, index=False, header=False)

        return transformed_table_path, transformed_msa_path, transformed_branch_lengths_path

    def get_data(self, table, msa, branch_lengths):
        tree_table = pd.read_csv(table, sep=',', header=None, names=['Parent', 'Child'])
        branch_lengths = pd.read_csv(branch_lengths, sep=',', header=None)
        branch_lengths = pd.DataFrame(branch_lengths.values.flatten(), columns=['Length'])
        msa = pd.read_csv(msa, sep=',', header=None)
        msa.columns = ['Species', 'Sequence']

        data = pd.concat([tree_table, branch_lengths], axis=1)
        data['Sequence'] = np.nan
        data['Sequence'] = data['Sequence'].astype(object)

        for index, row in msa.iterrows():
            child_value = row['Species']
            sequence_value = row['Sequence']
            data.loc[data['Child'] == child_value, 'Sequence'] = sequence_value
        return data

    def is_final_node(self, node_name):
        child_count = self.data['Child'].value_counts().get(node_name, 0)
        parent_count = self.data['Parent'].value_counts().get(node_name, 0)
        return child_count == 1 and parent_count == 0

    def populate_tree(self, data):
        nodes = {}

        for index, row in data.iterrows():
            parent = row['Parent']
            child = row['Child']
            branch_length = row['Length']
            sequence = row['Sequence']

            if parent not in nodes:
                nodes[parent] = Node(parent)
            if child not in nodes:
                nodes[child] = Node(child)

            nodes[child].parent = nodes[parent]
            nodes[child].branch_length = branch_length
            nodes[child].sequence = sequence
            nodes[child].is_final = self.is_final_node(child)
            nodes[parent].children.append(nodes[child])

        for node in nodes.values():
            if node.parent is None:
                self.root = node
                break
        self.nodes = nodes

    def one_hot_encode(self, sequence):
        if sequence is None or (isinstance(sequence, str) and sequence == ''):
            return np.array([])
        mapping = {
            'A': [1, 0, 0, 0],
            'C': [0, 1, 0, 0],
            'G': [0, 0, 1, 0],
            'T': [0, 0, 0, 1],
        }
        one_hot_sequence = [mapping[base] for base in sequence]
        return np.array(one_hot_sequence)

    def get_nucleotide_probability(self, node1, node2):
        prob_vector = []

        sequence1 = self.one_hot_encode(node1.sequence) if node1.is_final else node1.sequence
        sequence2 = self.one_hot_encode(node2.sequence) if node2.is_final else node2.sequence

        for i in range(len(sequence1)):
            exp_matrix1 = expm(self.transition_matrix * node1.branch_length)
            exp_matrix2 = expm(self.transition_matrix * node2.branch_length)
            transformed_seq1 = np.dot(exp_matrix1, sequence1[i])
            transformed_seq2 = np.dot(exp_matrix2, sequence2[i])
            prob_vector.append(transformed_seq1 * transformed_seq2)

        prob_vector = np.array(prob_vector)
        node1.parent.sequence = prob_vector
        return prob_vector

    def tree_probability(self, node):
        if node.is_final:
            # Leaf nodes already have sequences assigned
            return self.one_hot_encode(node.sequence)

        if not node.children:
            return None  # No children, no sequence to propagate

        # Recursively calculate probabilities for both children
        child_sequences = [self.tree_probability(child) for child in node.children if child.sequence is not None]

        if len(child_sequences) == 2:
            node.sequence = self.get_nucleotide_probability(node.children[0], node.children[1])
            return node.sequence
        else:
            return None

    def get_log_likelihood(self):
        eq_freq = np.array([0.25, 0.25, 0.25, 0.25])
        log_likelihood = np.sum(np.log(np.matmul(self.root.sequence, eq_freq)))
        return float(log_likelihood)

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        one_hot_sequence = self.one_hot_encode(node.sequence) if node.is_final and node.sequence else None
        print(
            ' ' * level * 4 + f'Node: {node.name}, Branch Length: {node.branch_length}, Sequence: {node.sequence}, One-Hot Encoded Sequence: {one_hot_sequence}, Is Final: {node.is_final}')
        for child in node.children:
            self.print_tree(child, level + 1)
