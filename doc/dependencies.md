
Table of Dependencies

See this for info on Markdown tables:
  <https://github.github.com/gfm/#tables-extension->

Updated in line with how the Makefile is current set up

$(ARCH) = 	rv\$(XLEN)\$(ISA)-\$(R_ABI)-\$(COMPILER)


|                   Dependencies                      |                     Recipes                      |                         Targets                           |
|-----------------------------------------------------|--------------------------------------------------|-----------------------------------------------------------|
| src/$(TEST_CASE).c, FNAME_DIRS | riscv$(XLEN)-unknown-elf-$(COMPILER) -[flags] -S | build/$(ARCH)/$(FNAME)/testcase.S |
|                                                     |                                                  |                                                           |
| src/$(TEST_CASE).c, FNAME_DIRS | riscv$(XLEN)-unknown-elf-$(COMPILER) -[flags] -c | build/$(ARCH)/$(FNAME)/testcase.o |
| src/common/syscalls.c | riscv$(XLEN)-unknown-elf-$(COMPILER) -[flags] -w -c | build/$(ARCH)/common/syscalls.o |
|                                                     |                                                  |                                                           |
| build/$(ARCH)/$(FNAME)/$(TEST_CASE).o, build/$(ARCH)/common/syscalls.o, src/common/entry.S, FNAME_DIRS | riscv$(XLEN)-unknown-elf-$(COMPILER) -[flags] -o | build/$(ARCH)/$(FNAME)/testcase.elf |
|                                                     |                                                  |                                                           |
| build/$(ARCH)/$(FNAME)/testcase.elf |              spike -l --isa=$(ISA)               |      build/$(ARCH)/$(FNAME)/nproc$(NPROC)/testcase.trc     |
|                                                     |                                                  |                                                           |
| build/$(ARCH)/$(FNAME)/testcase.elf, FNAME_DIRS |      riscv$(XLEN)-unknown-elf-objdump -S -D      |           build/$(ARCH)/$(FNAME)/testcase.dasm             |
|                                                     |                                                  |                                                           |
| build/$(ARCH)/$(FNAME)/testcase.elf, FNAME_DIRS |              spike -g --isa=$(ISA)               |           build/$(ARCH)/$(FNAME)/testcase.hst              |
|                                                     |                                                  |                                                           |
| build/$(ARCH)/$(FNAME)/testcase.dasm |                      sed -n                      |            build/$(ARCH)/$(FNAME)/main.dasm                |
|                                                     |                                                  |                                                           |
|build/$(ARCH)/$(FNAME)/main.dasm, build/$(ARCH)/$(FNAME)/nproc$(NPROC)/testcase.trc|                      sed -n                      |        build/$(ARCH)/$(FNAME)/nproc$(NPROC)/main.trc       |


