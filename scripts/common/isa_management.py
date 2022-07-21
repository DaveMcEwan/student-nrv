# Helper functions to manage the conversion of data from .isa CSV files into
#   data structures to be used in scripts

import csv

# Take in the input string detailing the ISA, parse it and grab the needed dictionaries.
# Also take in an optional keys argument which:
#   - can be left empty to indicate that we want all keys and their associated values
#   to be stored in the sub dictionary.
#   - if is a single string, returns a dictionary with only the value associated with
#   the key given by the string in it.
#   - if is a list of strings, returns a dictionary where each instruction key has a
#   sub dictionary where we can access multiple keys from the CSV file from.
def check_isa(isa, keys=None):    
    all_instrs = {}

    # Determine base instruction set based on the XLEN
    if int(isa[2:4]) == 32:
        all_instrs.update(convert_csv_to_dict("rv32", keys))
    else:
        # No file yet made for this condition
        all_instrs.update(convert_csv_to_dict("rv64", keys))
    
    # Include relevant instructions based on the remaining instructions
    # Dictionary to track what's been included
    history = { 'm' : False,
                'a' : False,
                'f' : False,
                'c' : False,
                'p' : False,
                'v' : False }
 
    for index in range(5, len(isa)):
        extension = isa[index].lower()
        # Possible base extensions : MAFCPV
        # Possible combinations : CD, CF (so far)
        if (history[extension]): # Extension already detected, ignore
            continue
        else: # New extension, check for combinations
            all_instrs.update(convert_csv_to_dict(isa[index]))
            history[isa[index]] = True
            if(extension == 'c'):
                if(history['f']):
                    all_instrs.update(convert_csv_to_dict('cf'))
            elif(extension == 'f'):
                if(history['c']):
                    all_instrs.update(convert_csv_to_dict('cf'))
        # Expand upon with more combinations as we make them

    # TODO : Consider extensions such as the bit manip ones which won't be 
    #   represented by just single characters.
    return all_instrs

# Function to take in a CSV file and convert it into the desired dictionary format
def convert_csv_to_dict(isa, key=None):
    test_dict = {}
    with open("isa/"+isa+".isa", 'r') as data_file:
        # Read in the data from the CSV file while ignoring comments 
        #   (beginning with a #) and ignoring empty lines
        data = csv.DictReader(filter(lambda row: row[0]!='#', data_file), \
        skipinitialspace=True, delimiter=',')

        for row in data:
            sub_dict = test_dict.get(row["Insn"], dict())
            if not key: # No key/key list given, form dictionary with all information
                for key in row.keys():
                    sub_dict[key] = row[key]
                test_dict[row["Insn"]] = sub_dict
            elif isinstance(key, str):
                test_dict[row["Insn"]] = int(row[key])
            elif isinstance(key, list):
                for k in key:
                    sub_dict[k] = row[k]
                test_dict[row["Insn"]] = sub_dict

    return test_dict

def main():
    dict_test = convert_csv_to_dict("cd", ["Ld", "St"])
    print(dict_test)

if __name__ == "__main__":
    main()