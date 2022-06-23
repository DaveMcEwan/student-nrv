# Instruction Trace analysis and display scripts

Each of the main non-display scripts parse the input instruction stream before acquiring specific information.

### /bandwidth
Contains scripts to output the byte stream (for either loading or storing) for an instruction trace. The associated display script then applies a moving average filter and visualises this byte stream using matplotlib in the form of a line graph.

### /insn_patterns
Scripts used to identify the most common instruction patterns. For sequences of size 2, there is a more optimised script (insn_pairs.py). Display scripts available to visualise the pattern distribution through a bar chart and heatmap.

To be continued...