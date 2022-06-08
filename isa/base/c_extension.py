all_dicts = {}
load_dict = {}
store_dict = {}

# Loads
c_sp_loads_dict = {  'c.lwsp': {'bytes': 4, 'cycles': 0}, 
                'c.ldsp': {'bytes': 8, 'cycles': 0},
                'c.lqsp': {'bytes': 16, 'cycles': 0},
                'c.flwsp': {'bytes': 4, 'cycles': 0},
                'c.fldsp': {'bytes': 8, 'cycles': 0}, }

load_dict.update(c_sp_loads_dict)
all_dicts.update(c_sp_loads_dict)

c_reg_loads_dict = { 'c.lw': {'bytes': 4, 'cycles': 0}, 
                'c.ld': {'bytes': 8, 'cycles': 0},
                'c.lq': {'bytes': 16, 'cycles': 0},
                'c.flw': {'bytes': 4, 'cycles': 0},
                'c.fld': {'bytes': 8, 'cycles': 0}, }
              
load_dict.update(c_reg_loads_dict)
all_dicts.update(c_reg_loads_dict)

# Stores
c_sp_stores_dict = {  'c.swsp': {'bytes': 4, 'cycles': 0}, 
                'c.sdsp': {'bytes': 8, 'cycles': 0},
                'c.sqsp': {'bytes': 16, 'cycles': 0},
                'c.fswsp': {'bytes': 8, 'cycles': 0},
                'c.fsdsp': {'bytes': 16, 'cycles': 0}, }

store_dict.update(c_sp_stores_dict)
all_dicts.update(c_sp_stores_dict)

c_reg_stores_dict = { 'c.sw': {'bytes': 4, 'cycles': 0}, 
                'c.sd': {'bytes': 8, 'cycles': 0},
                'c.sq': {'bytes': 16, 'cycles': 0},
                'c.fsw': {'bytes': 4, 'cycles': 0},
                'c.fsd': {'bytes': 8, 'cycles': 0}, }

store_dict.update(c_reg_stores_dict)
all_dicts.update(c_reg_stores_dict)