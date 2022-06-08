all_dicts = {}
load_dict = {}
store_dict = {}

base_loads_dict = {  'lw': {'bytes': 4, 'cycles': 0}, 
                'lh': {'bytes': 2, 'cycles': 0},
                'lhu': {'bytes': 2, 'cycles': 0},
                'lb': {'bytes': 1, 'cycles': 0},
                'lbu': {'bytes': 1, 'cycles': 0},}

load_dict.update(base_loads_dict)
all_dicts.update(base_loads_dict)

base_stores_dict = {  'sw': {'bytes': 4, 'cycles': 0}, 
                'sh': {'bytes': 2, 'cycles': 0},
                'sb': {'bytes': 1, 'cycles': 0},}

store_dict.update(base_stores_dict)
all_dicts.update(base_stores_dict)