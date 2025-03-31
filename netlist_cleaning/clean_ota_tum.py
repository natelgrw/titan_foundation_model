"""
clean_ota_tum_1.py

A Python script that iterates through set_1 of generated OTA_TUM .ckt 
netlists in OTA_TUM and reformats them in preparation for sizing and 
simulation in a Cadence Spectre environment. It is important to modify 
the absolute path name of the netlist to match your computer system, or 
else the netlist simulation will not work.

Author: Nathan Leung
Created: 3/1/2025
"""

import os

# modify path names to match personal computer system
NFET_PATH_NAME = '"/homes/natelgrw/Documents/TURBO_circuit_optimizer/lstp/7nfet.pm"'
PFET_PATH_NAME = '"/homes/natelgrw/Documents/TURBO_circuit_optimizer/lstp/7pfet.pm"'
    
def get_parameters(file_list):
    """
    Extracts circuit parameters for sizing from a .scs netlist file.
    
    Args:
        file_list (list): List of lines from a .scs netlist file.
    
    Returns:
        list: Sorted list of unique circuit parameters.
    """
    params = {"tempc={{tempc}}", "nA={{nA}}", "vcm={{vcm}}", "ibias={{ibias}}", "vdd={{vdd}}"}

    for line in file_list[1:]:
        tokens = line.split()
        if not tokens:
            continue
        
        # transistor components
        if "MM" in tokens[0]:
            for token in tokens[1:]:
                if token.startswith("nfin="):
                    param_name = f"nB{token[7:]}={{{{nB{token[7:]}}}}}"         
                else:
                    continue
                params.add(param_name)

        # capacitor components
        elif "C" in tokens[0]:
            params.add(f"nC{tokens[0][1:]}={{{{nC{tokens[0][1:]}}}}}")

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
    return [line for line in file_list if ("Transistor" in line or "Capacitor" in line)]

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
        if ".suckt" in elt:
            split_elt = elt.split()
            subcircuits.append(split_elt[1])
            edited_line_1 = elt.replace(".suckt", "subckt")
            edited_line_2 = edited_line_1.replace("sourceNmos sourcePmos", "gnd! vdd!")
            edited_list.append(edited_line_2)
        elif ".end" in elt:
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
    skip = False

    for i, line in enumerate(source_file_list):
        line_tokens = line.split()

        if not line_tokens:
            edited_list.append(line)
            continue

        if skip:
            skip = False
            continue

        if "Transistor" in line_tokens[0]:
            next_line_tokens = source_file_list[i + 1].split() if i + 1 < len(source_file_list) else []

            # standardize transistor types
            line_tokens = [f"MM{i}" if "NormalTransistor" in l else f"MM{i}" if "DiodeTransistor" in l 
                           else "nfet" if l.startswith("nmos") else "pfet" if l.startswith("pmos") 
                           else "vdd!" if l.startswith("sourcePmos") else "gnd!" if l.startswith("sourceNmos")
                           else l for l in line_tokens] + ["l=nA", "nfin=nA"]
            next_line_tokens = [f"MM{i + 1}" if "NormalTransistor" in l else f"MM{i + 1}" if "DiodeTransistor" in l
                                else "nfet" if l.startswith("nmos") else "pfet" if l.startswith("pmos") 
                                else "vdd!" if l.startswith("sourcePmos") else "gnd!" if l.startswith("sourceNmos")
                                else l for l in next_line_tokens] + ["l=nA", "nfin=nA"]

            if (next_line_tokens and next_line_tokens[0].startswith("MM") and 
                any(line_tokens[j] == next_line_tokens[j] for j in range(1, 4))):
                print(line_tokens[1], next_line_tokens[1])
                for tokens in (line_tokens, next_line_tokens):
                    for j, elt in enumerate(tokens):
                        if elt == "nfin=nA":
                            tokens[j] = f"nfin=nB{nfin_count}"
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

        elif "Capacitor" in line_tokens[0]:
            for i in range(len(line_tokens)):
                if line_tokens[i] == "sourcePmos":
                    line_tokens[i] = "vdd!"
                elif line_tokens[i] == "sourceNmos":
                    line_tokens[i] = "gnd!"
            number = line_tokens[0][9:]
            line_tokens[0] = f"C{number}"
            line_tokens.append("capacitor")
            line_tokens.append(f"c=nC{number}")
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
    cleaned_lines_1 = reformat_declarations(source_file_list)
    cleaned_lines_2 = edit_circuit_components(cleaned_lines_1)

    output.extend(cleaned_lines_2)

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
    output.append("I0 (ibias gnd!) isource dc=ibias type=dc")
    output.append("")

def append_combined_circuit_connections(output, source_file_list):
    """
    A function that cleans and edits a combined circuit declaration, 
    given an input list of subcircuits to add.
    """
    ckt_name = source_file_list[0].split()[1]
    output_dec = f"xi0 ibias in1 in2 out gnd! vdd! {ckt_name}"
    output.append(output_dec)

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

def append_save(output):
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
    
    append_cleaned_netlist(output_lines, input_lines)
    append_voltages(output_lines, input_lines)
    append_combined_circuit_connections(output_lines, input_lines)
    append_simulator_options(output_lines)
    append_save(output_lines)
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
        if filename.endswith(".ckt"):
            # Construct the full input and output file paths
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename.replace(".ckt", ".scs"))
            
            print(f"Processing file: {input_file}")
            # Process the file and save the output
            process_netlist(input_file, output_file)
            print(f"Saved cleaned netlist to: {output_file}")

if __name__ == "__main__":
    input_directory_1 = "OTA_TUM/OTATUM_set_1/ComplementaryOpAmp"
    input_directory_2 = "OTA_TUM/OTATUM_set_1/OneStageFullyDifferentialOpAmp"

    output_directory = "cleaned_ota_tum_netlists"

    process_all_files(input_directory_1, output_directory)
    process_all_files(input_directory_2, output_directory)
    

    # Process all files in the directory
    # process_all_files(input_directory, output_directory)
    

    


