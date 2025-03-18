"""
clean_gana.py

A Python script that iterates through a series of generated GANA .sp 
netlists in FULL_OTA and reformats them in preparation for sizing and 
simulation in a Cadence Spectre environment. It is important to modify 
the absolute path name of the netlist to match your computer system, or 
else the netlist simulation will not work.

Author: Nathan Leung
Created: 2/23/2025
"""
import os
import re

# modify path names to match personal computer system
NFET_PATH_NAME = '"/homes/natelgrw/Documents/TURBO_circuit_optimizer/lstp/7nfet.pm"'
PFET_PATH_NAME = '"/homes/natelgrw/Documents/TURBO_circuit_optimizer/lstp/7pfet.pm"'

def get_full_path(folder, filename):
    """
    Constructs the full file path by joining the specified folder and filename.
    Checks if the file exists at the given location.

    Args:
        folder (str): The path to the folder containing the file.
        filename (str): The name of the file.

    Returns:
        str: The full file path if the file exists, otherwise an error message.
    """
    full_path = os.path.join(folder, filename)
    
    if os.path.isfile(full_path):
        return full_path
    else:
        return f"The file {filename} does not exist in the folder {folder}."
    
def get_parameters(file_list):
    """
    Extracts circuit parameters for sizing from a .scs netlist file.
    
    Args:
        file_list (list): List of lines from a .scs netlist file.
    
    Returns:
        list: Sorted list of unique circuit parameters.
    """
    params = {"tempc={{tempc}}", "nA={{nA}}", "vcm={{vcm}}"}
    r_counter, c_counter = -1, -1

    for line in file_list:
        tokens = line.split()
        if not tokens:
            continue
        
        # transistor components
        first_token = tokens[0]
        if first_token.startswith("MM"):
            for token in tokens[1:]:
                if token.startswith("nfin="):
                    param_name = f"nB{token[7:]}={{{{nB{token[7:]}}}}}"
                elif not any(x in token for x in 
                    ("net", "gnd", "nmos", "pmos", "w=", "l=", "Vin", "Vout", "nfet", "pfet")):
                    param_name = f"{token.lower().replace('!', '')}={{{{{token.lower().replace('!', '')}}}}}"
                else:
                    continue
                params.add(param_name)
        
        # resistor components
        elif first_token.startswith("R"):
            r_counter += 1
            params.add(f"nR{r_counter}={{{{nR{r_counter}}}}}")

        # capacitor components
        elif first_token.startswith("C"):
            c_counter += 1
            params.add(f"nC{c_counter}={{{{nC{c_counter}}}}}")

    return sorted(params)

def get_components(file_list):
    """
    Takes in a list representing .scs netlist lines and returns
    a list of circuit components in the netlist.

    Args:
        file_list (list): A list containing read .scs netlist lines.

    Returns:
        list: A list of circuit component lines that start with "MM", "RR", or "CC".
    """
    return [line for line in file_list if line.startswith(("MM", "RR", "CC"))]

def append_setup(output, source_file_list):
    """
    Appends appropriate setup protocol lines to a list
    for reading and writing to a new file.

    Args:
       output (list): an empty list
       source_file_list (list): a list produced from reading a GANA .sp file
    """
    output.append("simulator lang=spectre")
    output.append("global 0")

    param_list = get_parameters(source_file_list)
    param_str = "parameters "
    for elt in param_list:
        param_str += (elt + " ")

    output.append(param_str)
    nfet_path_name_str = "include " + NFET_PATH_NAME
    pfet_path_name_str = "include " + PFET_PATH_NAME
    output.append(nfet_path_name_str)
    output.append(pfet_path_name_str)
    output.append("")

def remove_comments_and_params(source_file_list):
    """
    Removes lines starting with `*` or containing ".PARAMS" from the source file list.

    Args:
        source_file_list (list): List of lines from the input file.

    Returns:
        list: Filtered list of lines without comments or ".PARAM".
    """
    cleaned_list = []
    for line in source_file_list:
        if line.startswith("*"):
            continue 
        elif ".PARAM" in line:
            continue
        elif "+    " in line:
            continue
        cleaned_list.append(line.strip())

    filtered_list = []
    for line in cleaned_list:
        if line or (filtered_list and filtered_list[-1]):
            filtered_list.append(line)

    return filtered_list

def reformat_declarations(source_file_list):
    """
    Reformats subcircuit definitions to fit spectre netlist syntax.

    Args:
        source_file_list (list): List of lines from the input file.

    Returns:
        list: Updated list of lines with the specified replacements.
    """
    subcircuits = []
    edited_list = []
    for elt in source_file_list:
        if ".SUBCKT" in elt:
            split_elt = elt.split()
            subcircuits.append(split_elt[1])
            edited_line = elt.replace(".SUBCKT", "subckt")
            edited_list.append(edited_line.replace("/ ", ""))
        elif ".ENDS" in elt:
            subckt_name = subcircuits.pop(0) if len(subcircuits) > 0 else None
            edited_line = "ends " + subckt_name
            edited_list.append(edited_line.replace("/ ", ""))
        else:
            edited_list.append(elt.replace("/ ", ""))

    return edited_list

def edit_circuit_components(source_file_list):
    """
    Modifies circuit components in a netlist by standardizing transistor labels, 
    updating parameter values, and removing unnecessary width specifications.

    Args:
        source_file_list (list): A list of strings representing the lines of a netlist.

    Returns:
        list: A modified list of netlist lines with updated component parameters.
    """
    edited_list = []
    nfin_count = 0
    resistor_counter = 0  # Counter for resistors
    skip = False

    for i, line in enumerate(source_file_list):
        line_tokens = line.split()

        if not line_tokens:
            edited_list.append(line)
            continue

        if skip:
            skip = False
            continue

        if line_tokens[0].startswith("MM"):
            next_line_tokens = source_file_list[i + 1].split() if i + 1 < len(source_file_list) else []

            # Standardize transistor types
            line_tokens = ["l=nA" if l.startswith("l=") else "nfet" if l.startswith("nmos") 
                           else "pfet" if l.startswith("pmos") else l for l in line_tokens]
            next_line_tokens = ["l=nA" if l.startswith("l=") else "nfet" if l.startswith("nmos") 
                                else "pfet" if l.startswith("pmos") else l for l in next_line_tokens]

            if (next_line_tokens and next_line_tokens[0].startswith("MM") and 
                any(line_tokens[j] == next_line_tokens[j] for j in range(1, 4))):
                for tokens in (line_tokens, next_line_tokens):
                    for j, elt in enumerate(tokens):
                        if elt == "nfin=nA":
                            tokens[j] = f"nfin=nB{nfin_count}"
                        elif elt.startswith("w="):
                            tokens[j] = ""  
                nfin_count += 1
                edited_list.append(" ".join(filter(None, line_tokens)))
                edited_list.append(" ".join(filter(None, next_line_tokens)))
                skip = True
            else:
                for j, elt in enumerate(line_tokens):
                    if elt == "nfin=nA":
                        line_tokens[j] = f"nfin=nB{nfin_count}"
                    elif elt.startswith("w="):
                        line_tokens[j] = ""
                nfin_count += 1
                edited_list.append(" ".join(filter(None, line_tokens)))

        elif line_tokens[0].startswith("RR"):
            # Update resistor parameters
            number = line_tokens[0][2:]
            # Change "RR{number}" to "R{number}"
            line_tokens[0] = f"R{number}"
            # Insert "resistor" before the last element
            line_tokens.insert(-1, "resistor")
            # Parameterize the resistance value
            line_tokens[-1] = f"r=nR{resistor_counter}"
            resistor_counter += 1
            edited_list.append(" ".join(line_tokens))

        elif line_tokens[0].startswith("CC"):
            # Update capacitor parameters
            number = line_tokens[0][2:]
            # Change "CC{number}" to "C{number}"
            line_tokens[0] = f"C{number}"
            # Insert "capacitor" before the last element
            line_tokens.insert(-1, "capacitor")
            # Parameterize the capacitance value
            line_tokens[-1] = f"c=nC{number}"
            edited_list.append(" ".join(line_tokens))

        else:
            edited_list.append(line)

    return edited_list

def append_cleaned_netlist(output, source_file_list):
    """
    Cleans the netlist by processing lines with remove_comments_and_params and adding them to output.

    Args:
        output (list): List to store cleaned lines.
        source_file_list (list): List of lines from the input file.
    """
    cleaned_lines_1 = remove_comments_and_params(source_file_list)
    cleaned_lines_2 = reformat_declarations(cleaned_lines_1)
    cleaned_lines_3 = edit_circuit_components(cleaned_lines_2)
    cleaned_lines_4 = cleaned_lines_3[:-4] if len(cleaned_lines_3) >= 4 else []

    output.extend(cleaned_lines_4)

def append_voltages(output, source_file_list):
    """
    Appends voltage assignments to a list representing 
    a gana op-amp netlist.

    Args:
        output (list): an empty list
        source_file_list (list): a list produced from reading a GANA .sp file
    """
    
    output.append("VS (gnd! 0) vsource dc=0 type=dc")
    output.append("V0 (vdd! gnd!) vsource dc=vdd type=dc")
    output.append("V2 (in gnd!) vsource type=dc mag=1")
    output.append("E1 (Vinp cm in gnd!) vcvs gain=.5")
    output.append("E0 (Vinn cm in gnd!) vcvs gain=-0.5")
    output.append("V1 (cm gnd!) vsource dc=vcm type=dc")

    params = get_parameters(source_file_list)

    vbiasp_numbers = []
    vbiasn_numbers = []
    biasp_numbers = []
    biasn_numbers = []

    for param in params:
        # match vbiasp, vbiasn, biasp, biasn followed by a number or without a number
        match_vbiasp = re.match(r"vbiasp(\d*)", param)
        match_vbiasn = re.match(r"vbiasn(\d*)", param)
        match_biasp = re.match(r"biasp(\d*)", param)
        match_biasn = re.match(r"biasn(\d*)", param)

        if match_vbiasp:
            number = match_vbiasp.group(1) if match_vbiasp.group(1) else "0"
            vbiasp_numbers.append(number)
        
        if match_vbiasn:
            number = match_vbiasn.group(1) if match_vbiasn.group(1) else "0"
            vbiasn_numbers.append(number)
        
        if match_biasp:
            number = match_biasp.group(1) if match_biasp.group(1) else "0"
            biasp_numbers.append(number)
        
        if match_biasn:
            number = match_biasn.group(1) if match_biasn.group(1) else "0"
            biasn_numbers.append(number)

    # append the voltage sources for vbiasp
    for number in vbiasp_numbers:
        if number == "0":
            output.append(f"VP{number} (Vbiasp gnd!) vsource dc=vbiasp type=dc")
        else:
            output.append(f"VP{number} (Vbiasp{number} gnd!) vsource dc=vbiasp{number} type=dc")

    # append the voltage sources for vbiasn
    for number in vbiasn_numbers:
        if number == "0":
            output.append(f"VN{number} (Vbiasn gnd!) vsource dc=vbiasn type=dc")
        else:
            output.append(f"VN{number} (Vbiasn{number} gnd!) vsource dc=vbiasn{number} type=dc")

    # append the voltage sources for biasp
    for number in biasp_numbers:
        if number == "0":
            output.append(f"BP{number} (Biasp gnd!) vsource dc=biasp type=dc")
        else:
            output.append(f"BP{number} (Biasp{number} gnd!) vsource dc=biasp{number} type=dc")

    # append the voltage sources for biasn
    for number in biasn_numbers:
        if number == "0":
            output.append(f"BN{number} (Biasn gnd!) vsource dc=biasn type=dc")
        else:
            output.append(f"BN{number} (Biasn{number} gnd!) vsource dc=biasn{number} type=dc")

    output.append("")

def append_combined_circuit_connections(output, source_file_list):
    """
    A function that cleans and edits a combined circuit declaration, 
    given an input list of subcircuits to add.
    """
    dec_list = []
    for i, elt in enumerate(source_file_list):
        if elt.startswith(".SUBCKT") and source_file_list[i + 1].startswith("+"):
            dec_list.append(elt[8:-1] + source_file_list[i + 1][1:-2])
        elif elt.startswith(".SUBCKT"):
            dec_list.append(elt[8:-1])
    
    for i, elt in enumerate(dec_list):
        dec_split = elt.split()
        output_list = [f"xi{i}"] + dec_split[1:] + [dec_split[0]]
        output.append(" ".join(output_list))

def append_simulator_options(output):
    """
    Appends simulator options protocol lines to a list
    for reading and writing to a new file.

    Args:
       output (list): an empty list
       source_file_list (list): a list produced from reading a GANA .sp file
    """
    output.append("")
    output.append("simulatorOptions options psfversion=\"1.4.0\" reltol=1e-3 vabstol=1e-6 \\")
    output.append("    iabstol=1e-12 temp=tempc tnom=27 scalem=1.0 scale=1.0 gmin=1e-12 rforce=1 \\")
    output.append("    maxnotes=5 maxwarns=5 digits=5 cols=80 pivrel=1e-3 \\")
    output.append("    sensfile=\"../psf/sens.output\" checklimitdest=psf")
    output.append("    ac ac start=1 stop=100G dec=10 annotate=status")
    output.append("dcOp dc write=\"spectre.dc\" maxiters=150 maxsteps=10000 annotate=status")
    output.append("dcOpInfo info what=oppoint where=rawfile")
    output.append("modelParameter info what=models where=rawfile")
    output.append("element info what=inst where=rawfile")
    output.append("outputParameter info what=output where=rawfile")
    output.append("designParamVals info what=parameters where=rawfile")
    output.append("primitives info what=primitives where=rawfile")
    output.append("subckts info what=subckts where=rawfile")

def append_save(output, components):
    """
    Appends save protocol lines to a list
    for reading and writing to a new file.

    Args:
       output (list): an empty list
       parameters (list): a list of netlist paramet
    """
    output.append("saveOptions options save=allpub")
  
def process_netlist(input_file, output_file):
    """ 
    Takes in a GANA .sp netlist and writes a reformatted and cleaned
    .scs netlist that can be used for simulation and sizing in Cadence 
    Spectre environments into a cleaned_gana_netlists folder.

    Args:
        input_file (str): a relative file path name for a GANA .sp netlist
        output_file (str): a relative file path name for the output .scs netlist
    """
    with open(input_file) as file:
        input_lines = file.readlines()

    output_lines = []
    setup_lines = []
    comps = get_components(input_lines)
    
    append_cleaned_netlist(output_lines, input_lines)
    append_voltages(output_lines, input_lines)
    append_combined_circuit_connections(output_lines, input_lines)
    append_simulator_options(output_lines)
    append_save(output_lines, comps)
    append_setup(setup_lines, output_lines)

    output_lines = setup_lines + output_lines[:]

    with open(output_file, "w") as file:
        for str_line in output_lines:
            file.write(str_line + "\n")

def process_all_files(input_dir, output_dir):
    """
    Iterates through all .sp files in the input directory and processes them,
    saving the output as .scs files in the output directory.

    Args:
        input_dir (str): The directory containing the .sp files.
        output_dir (str): The directory where the cleaned .scs files will be saved.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Iterate through all files in the input directory
    for filename in os.listdir(input_dir):
        # Check if the file is a .sp file
        if filename.endswith(".sp"):
            # Construct the full input and output file paths
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename.replace(".sp", ".scs"))
            
            print(f"Processing file: {input_file}")
            # Process the file and save the output
            process_netlist(input_file, output_file)
            print(f"Saved cleaned netlist to: {output_file}")

if __name__ == "__main__":
    input_directory = "GANA_OTATUM_circuit_data/circuit_data/source_files/dataset_generator/ota_data_generator/FULL_OTA"
    output_directory = "cleaned_gana_netlists"
    
    # Process all files in the directory
    process_all_files(input_directory, output_directory)
    

    


