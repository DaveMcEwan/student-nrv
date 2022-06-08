all_dicts = {}

c_sp_loads_dict = {  'c.lwsp': {'bytes': 4, 'cycles': 0}, 
                'c.ldsp': {'bytes': 8, 'cycles': 0},
                'c.lqsp': {'bytes': 16, 'cycles': 0},
                'c.flwsp': {'bytes': 4, 'cycles': 0},
                'c.fldsp': {'bytes': 8, 'cycles': 0},
             }

c_reg_loads_dict = { 'c.lw': {'bytes': 4, 'cycles': 0}, 
                'c.ld': {'bytes': 8, 'cycles': 0},
                'c.lq': {'bytes': 16, 'cycles': 0},
                'c.flw': {'bytes': 4, 'cycles': 0},
                'c.fld': {'bytes': 8, 'cycles': 0},
              }
              
all_dicts.update(c_sp_loads_dict)
all_dicts.update(c_reg_loads_dict)