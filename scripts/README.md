# Instruction Trace analysis and display scripts

This details the scripts currently available here.

Scripts written work together with CSV files located in [isa/](isa/) which detail information about each instruction that we can look at in our scripts. Functions that parse informatiom from these CSV files to then be used in scripts are found in /common/isa_management.py. For more details on the CSV files, please read [isa/README.md](isa/README.md). Overall, for more information on the individual scripts, please refer to the comments on the scripts themselves which contain an initial description at the beginning of each script.

## /common
Folder used for general-purpose scripts which you may find useful or want to take the output from.

## /display
Folder for general display scripts. Each display script takes an input JSON file so please ensure your scripts output JSON files of the correct format. Additionally, they use a profile system detailed by the -p/--profile flag which you can use to automatically assign things like axis names and graph titles.

### /bandwidth
Scripts to look at the bandwidth stream for load and store instructions and visualise them using line graphs.

### /insn_patterns
Scripts used to identify the most common instruction pairs and patterns in the range from 3 to 8. Then visualised through a column graph (for pairs and patterns) and a heatmap (for pairs only).

### /reg_accesses
Scripts used to look at the register activity and count how often each register has been read from and written to.