# rv32ic

# Categories
all_dicts = {}
load_dict = {}
store_dict = {}

def update_dicts(module_name):
    all_dicts.update(module_name.all_dicts)
    load_dict.update(module_name.load_dict)
    store_dict.update(module_name.store_dict)

# Import the base 32i instructions
import base.rv32i
update_dicts(base.rv32i)

# Import the C instructions
import base.c_extension
update_dicts(base.c_extension)
