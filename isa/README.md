# isa
This directory contains the CSV files (with the suffix .isa) which contains the instructions and information associated with them in a file named after the extension they come from. Base instructions are available in rv32.isa.

**/reg** contains files which just lists the registers available for each extension using their ABI names rather than their actual register values e.g. 'x0' is written as 'zero' as this is how Spike writes it in the output instruction trace.

Note that the naming convention for the 'Type' column took a lot of influence from the [RISC-V reference card](https://www.cl.cam.ac.uk/teaching/1617/ECAD+Arch/files/docs/RISCVGreenCardv8-20151013.pdf).