# isa
This directory contains the CSV files (with the suffix .isa) which contains the instructions and information associated with them in a file named after the extension they come from. Base instructions are available in rv32.isa.

**/reg** contains files which just lists the registers available for each extension using their ABI names rather than their actual register values e.g. 'x0' is written as 'zero' as this is how Spike writes it in the output instruction trace.