
Table of Dependencies

See this for info on Markdown tables:
  <https://github.github.com/gfm/#tables-extension->

Updated in line with how the Makefile is current set up

<Arch> = 	rv$(XLEN)$(ISA)-$(R_ABI)-$(COMPILER)


|                   Dependencies                      |                     Recipes                      |                         Targets                           |
|-----------------------------------------------------|--------------------------------------------------|-----------------------------------------------------------|
|             test_case/$(TEST_CASE).c                | riscv$(XLEN)-unknown-elf-$(COMPILER) -[flags] -S |          build/<Arch>/$(FNAME)/testcase.S                 |
|                                                     |                                                  |                                                           |
|             test_case/$(TEST_CASE).c                | riscv$(XLEN)-unknown-elf-$(COMPILER) -[flags] -c |          build/<Arch>/$(FNAME)/testcase.o                 |
|                                                     |                                                  |                                                           |
|       build/<Arch>/$(FNAME)/$(TEST_CASE).o          | riscv$(XLEN)-unknown-elf-$(COMPILER) -[flags] -o |           build/<Arch>/$(FNAME)/testcase.elf              |
|           build/<Arch>/common/syscalls.o            |                                                  |                                                           |
|                   src/entry.S                       |                                                  |                                                           |
|                                                     |                                                  |                                                           |
|         build/<Arch>/$(FNAME)/testcase.elf          |              spike -l --isa=$(ISA)               |      build/<Arch>/$(FNAME)/nproc$(NPROC)/testcase.trc     |
|                                                     |                                                  |                                                           |
|         build/<Arch>/$(FNAME)/testcase.elf          |      riscv$(XLEN)-unknown-elf-objdump -S -D      |           build/<Arch>/$(FNAME)/testcase.dasm             |
|                                                     |                                                  |                                                           |
|         build/<Arch>/$(FNAME)/testcase.elf          |              spike -g --isa=$(ISA)               |           build/<Arch>/$(FNAME)/testcase.hst              |
|                                                     |                                                  |                                                           |
|         build/<Arch>/$(FNAME)/testcase.dasm         |                      sed -n                      |            build/<Arch>/$(FNAME)/main.dasm                |
|                                                     |                                                  |                                                           |
|           build/<Arch>/$(FNAME)/main.dasm           |                      sed -n                      |        build/<Arch>/$(FNAME)/nproc$(NPROC)/main.trc       |
|   build/<Arch>/$(FNAME)/nproc$(NPROC)/testcase.trc  |                                                  |                                                           |
|                                                     |                                                  |                                                           |


