
Table of Dependencies

See this for info on Markdown tables:
  <https://github.github.com/gfm/#tables-extension->

Updated in line with how the Makefile is current set up

|               Dependencies             |                     Recipes                      |                         Targets                           |
|----------------------------------------|--------------------------------------------------|-----------------------------------------------------------|
|       test_case/$(TEST_CASE).c         | riscv$(XLEN)-unknown-elf-$(COMPILER) -[flags] -S |          build/<Arch>/<TestCase>/$(TEST_CASE).S           |
|                                        |                                                  |          build/<Arch>/<TestCase>/$(TEST_CASE).o           |
|                                        |                                                  |                                                           |
| build/<Arch>/<TestCase>/$(TEST_CASE).o |  riscv[bits]-unknown-elf-[compiler] -[flags] -o  |           build/<Arch>/<TestCase>/testcase.elf            |
|     build/<Arch>/common/syscalls.o     |                                                  |                                                           |
|             src/entry.S                |                                                  |                                                           |
|                                        |                                                  |                                                           |
|  build/<Arch>/<TestCase>/testcase.elf  |              spike -l --isa=[flag]               |   build/<Arch>/<TestCase>/nproc$(NPROC)/instr-trace.trc   |



