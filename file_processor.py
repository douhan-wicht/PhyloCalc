def adapt_files(msa_new_file, table_new_file, branch_length_new_file, output_msa, output_table, output_branch_length):
    """
    Adapt msa_new.dat, table_new.dat, and branch_length_new.dat to their original formats.

    Parameters:
        msa_new_file (str): Path to the msa file (msa_new.dat).
        table_new_file (str): Path to the table file (table_new.dat).
        branch_length_new_file (str): Path to the branch length file (branch_length_new.dat).
        output_msa (str): Path to save the adapted msa.dat file.
        output_table (str): Path to save the adapted table.dat file.
        output_branch_length (str): Path to save the adapted branch_length.dat file.
    """
    try:
        # Step 1: Process msa_new.dat
        species_to_id = {}  # Mapping of species names to numeric IDs
        msa_lines = []  # Lines for the adapted msa.dat file
        species_counter = 1  # Start numbering from 1

        with open(msa_new_file, 'r') as msa_file:
            for line in msa_file:
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    species_name, sequence = parts
                    if species_name not in species_to_id:
                        species_to_id[species_name] = species_counter
                        species_counter += 1
                    numeric_id = species_to_id[species_name]
                    msa_lines.append(f"{numeric_id} {sequence}")

        # Save the adapted msa.dat
        with open(output_msa, 'w') as msa_out:
            msa_out.write("\n".join(msa_lines))

        print(f"msa.dat created successfully at {output_msa}")

        # Step 2: Process table_new.dat
        table_lines = []  # Lines for the adapted table.dat file
        with open(table_new_file, 'r') as table_file:
            for line in table_file:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    parent, child = parts
                    # Replace species names with their IDs if they exist in the mapping
                    parent = species_to_id.get(parent, parent)
                    child = species_to_id.get(child, child)
                    table_lines.append(f"{parent},{child}")

        # Save the adapted table.dat
        with open(output_table, 'w') as table_out:
            table_out.write("\n".join(table_lines))

        print(f"table.dat created successfully at {output_table}")

        # Step 3: Process branch_length_new.dat
        # Assuming branch_length_new.dat has the same structure as the original, we just copy it over
        with open(branch_length_new_file, 'r') as branch_length_file:
            branch_length_content = branch_length_file.read()

        with open(output_branch_length, 'w') as branch_length_out:
            branch_length_out.write(branch_length_content)

        print(f"branch_length.dat created successfully at {output_branch_length}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
# adapt_files("input_data/training.msa.dat", "input_data/training.table.dat", "input_data/training.branchlength.dat", "taining-output.msa.dat", "training-output.table.dat", "training-output.branchlength.dat")
adapt_files("input_data/ENSG00000013016_EHD3_NT.msa.dat", "input_data/ENSG00000013016_EHD3_NT.table.dat", "input_data/ENSG00000013016_EHD3_NT.branchlength.dat", "taining-output.msa.dat", "training-output.table.dat", "training-output.branchlength.dat")