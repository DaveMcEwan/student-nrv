# Checks if an item is in the input dictionary and increments
#   if it is or creates a key if it doesn't exist
def append_to_counter_dict(dct, insn_name):
    if insn_name in dct:
        dct[insn_name] += 1
    else:
        dct[insn_name] = 1