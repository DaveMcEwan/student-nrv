#******************************************************************************
#    Expanding upon the repo by Noureddine Ait Said : https://github.com/noureddine-as/riscv-baremetal-DefaultConfig
#------------------------------------------------------------------------------

.SECONDARY: # Used to stop make from deleting intermediate files

# default: build
# default: sim
default: disassembly
default: histogram
default: extract_main

# Checking if a RISCV compiler is present
ifndef RISCV
$(error "[ ERROR ] - RISCV variable not set!")
endif

# Macro definitions for directories to be used in the compile lines
SRC_DIR = ./src
BUILD_DIR = ./build

INCLUDES = -I./include

TEST_CASES = ./test_cases
LINKER_SCRIPT = link.ld

MK_CSV :=  ./csv/csv.mk
CSV ?= ./csv/config5.csv

$(shell echo CSV FNAME currently set to : ${CSV})

include ${MK_CSV}

# ----- Variables based on the CSV - Used for initial directory formatting -----
R_XLEN		= $(call CSV_COL,1,${row})
R_COMPILER	= $(call CSV_COL,2,${row})
R_ISA		= $(call CSV_COL,3,${row})
R_ABI		= $(call CSV_COL,4,${row})
R_NPROC 	= $(call CSV_COL,5,${row})
R_FNAME		= $(call CSV_COL,6,${row})

#	Forming the targets
# Target instruction trace, based on the CSV values
TRACES := $(foreach row,${CSV_ROWS},$\
	${BUILD_DIR}/$\
	rv$(call R_XLEN)$(call R_ISA)-$(call R_ABI)-$(call R_COMPILER)/$\
	$(call R_FNAME)/nproc-$(call R_NPROC)/instr-trace.trc)

# 	Form the other targets using string manipulation with the current target
MAIN_TRACES := $(subst instr-trace,main-instr-trace,${TRACES})

# Go up one directory - places us in the FNAME directory
NPROC_DIRS := $(dir ${TRACES})
FNAME_DIRS := $(addsuffix ../,${NPROC_DIRS})

HISTOGRAMS := $(addsuffix histogram.hst,${FNAME_DIRS})
OBJECTS := $(addsuffix testcase.o,${FNAME_DIRS}) # ${BUILD_DIR}/%/testcase.o
EXECUTABLES := $(addsuffix testcase.elf,${FNAME_DIRS})
DISASSEMBLIES := $(addsuffix disassembly.dasm,${FNAME_DIRS})
MAIN_DISASSEMBLIES := $(subst disassembly, main-disassembly,${DISASSEMBLIES})

# ----- Variable definitions based on the pattern rule -----
# Example directory name : rv32gc-ilp32-gcc/printf/nproc-2/
DIRNAME_SPLIT1 = $(subst -,$(space),$*)
DIRNAME_SPLIT2 = $(subst /,$(space), $(DIRNAME_SPLIT1))
# The example at this point would then be : rv32gc ilp32 gcc printf nproc 2
ISA 		= $(word 1, $(DIRNAME_SPLIT2))
ABI			= $(word 2, $(DIRNAME_SPLIT2))
COMPILER 	= $(word 3, $(DIRNAME_SPLIT2))
FNAME 		= $(word 4, $(DIRNAME_SPLIT2))
# The 5th word is nproc; no information we can take from this
N_PROC 		= $(word 6, $(DIRNAME_SPLIT2))

# If there is a '32' present in rv__, set XLEN to it. 
#	Else set it to 64 if that is present
XLEN 	 	= $(findstring 32, ${ISA})
XLEN 	 	?= $(findstring 64, ${ISA})

# Form the compilation command
CC = riscv$(XLEN)-unknown-elf-$(COMPILER)

OBJDUMP = $(RISCV)/bin/riscv$(XLEN)-unknown-elf-objdump
SIZE 	= $(RISCV)/bin/riscv$(XLEN)-unknown-elf-size
SPIKE 	= $(RISCV)/bin/spike

# Default compiler flags
CFLAGS = -march=$(ISA)
CFLAGS += -mabi=$(ABI)
CFLAGS += -mcmodel=medany
CFLAGS += -ffreestanding
CFLAGS += -static
CFLAGS += -nostdlib
CFLAGS += -nostartfiles 
CFLAGS += -lgcc

LDFLAGS = -T${LINKER_SCRIPT}

#	Testing
print_all: TRACES
	@echo TRACES
	@echo ${TRACES}
	@echo
	@echo MAIN_TRACES
	@echo ${MAIN_TRACES}
	@echo
	@echo NPROC_DIRS
	@echo ${NPROC_DIRS}
	@echo
	@echo FNAME_DIRS
	@echo ${FNAME_DIRS}
	@echo
	@echo HISTOGRAMS
	@echo ${HISTOGRAMS}
	@echo
	@echo OBJECTS
	@echo ${OBJECTS}
	@echo
	@echo EXECUTABLES
	@echo ${EXECUTABLES}
	@echo
	@echo DISASSEMBLIES
	@echo ${DISASSEMBLIES}
	@echo
	@echo MAIN_DISASSEMBLIES
	@echo ${MAIN_DISASSEMBLIES}

TRACES:
	mkdir -p $(FNAME_DIRS)

.PHONY: build
build: $(EXECUTABLES)

# Executable target
# example $* = rv32gc-ilp32-gcc/simple_add/nproc-1/..
# https://www.gnu.org/software/make/manual/html_node/Prerequisite-Types.html
${BUILD_DIR}/%/testcase.elf: ${BUILD_DIR}/%/testcase.o \
	$(BUILD_DIR)/%/../common/syscalls.o

	$(CC) $^ ${SRC_DIR}/entry.S $(CFLAGS) ${INCLUDES} $(LDFLAGS) -o $@

# Bottom of the dependency tree
# Secondary expansion used to access the pattern rule in the dependency list
.SECONDEXPANSION:
$(BUILD_DIR)/%/testcase.o: \
	$$(addsuffix .c,$$(addprefix ./test_cases/,$$(word 2, $$(subst /, ,$$*))))
	
	mkdir -p $(dir $@)
	$(CC) $(CFLAGS) ${INCLUDES} -c $^ -o $@

# Producing the assembly FNAME for debugging
# $(CC) $(CFLAGS) ${INCLUDES} -S ${TEST_CASES}/$(FNAME).c -o ${BUILD_DIR}/$*/testcase.S
# TODO : Add assembly file target and recipe

$(BUILD_DIR)/%/../common/syscalls.o: ${SRC_DIR}/syscalls.c
	mkdir -p $(dir $@)
	$(CC) $(CFLAGS) ${INCLUDES} -w -c $< -o $@

# --------------- INSTRUCTION TRACE, DISASSEMBLY and HISTOGRAM ---------------
.PHONY: sim
sim: $(TRACES)

# $(addsuffix $(dir ${BUILD_DIR}/%), /testcase.elf)
${BUILD_DIR}/%/instr-trace.trc: ${BUILD_DIR}/%/../testcase.elf
	mkdir -p $(dir $@)
	$(SPIKE) -p$(N_PROC) -l --isa=$(ISA) $< 2> $@

.PHONY: disassembly
disassembly: $(DISASSEMBLIES)

${BUILD_DIR}/%/disassembly.dasm: ${BUILD_DIR}/%/testcase.elf
	mkdir -p $(dir $@)
	$(OBJDUMP) -S -D $< > $@

.PHONY: histogram
histogram: $(HISTOGRAMS)

${BUILD_DIR}/%/histogram.hst: ${BUILD_DIR}/%/testcase.elf
	mkdir -p $(dir $@)
	$(SPIKE) -g --isa=$(ISA) $< 2> $@

.PHONY: extract_main
extract_main: $(MAIN_TRACES)

${BUILD_DIR}/%/main-instr-trace.trc: ${BUILD_DIR}/%/../main-disassembly.dasm ${BUILD_DIR}/%/instr-trace.trc
	mkdir -p $(dir $@)
	$(eval START_ADDRESS = $(shell cat $< | head -n1 | awk '{print $$1;}'))
	$(eval END_ADDRESS = $(shell cat $< | tail -n1 | awk '{print $$1;}' | tr -d ':'))
	sed -n '/$(START_ADDRESS)/,/$(END_ADDRESS)/p' ${BUILD_DIR}/$*/instr-trace.trc > $@

${BUILD_DIR}/%/../main-disassembly.dasm: ${BUILD_DIR}/%/../disassembly.dasm
	sed -n '/<main>:/,/ret/p' $< > $@

# ----------------------- CLEAN -----------------------
.PHONY: clean
clean:
	rm -r ${BUILD_DIR}

###################################################################################
# # Spike with GDB
# .PHONY: debug
# debug:
# 	@echo "-------------------  Starting Debugging  -------------------"
# 	@$(SPIKE) -d -p$(N_PROC) --isa=$(ISA) $(TARGET).elf

# # Build and simulate (build is forced by having the .elf dependency?)
# .PHONY: build-sim
# build-sim: $(TARGET).elf
# 	@echo ""
# 	@echo "-------------  Build done, starting simulation  -------------"
# 	@$(SPIKE) -p$(N_PROC) --isa=$(ISA)  $(TARGET).elf

# # ${BUILD_DIR}/%/<log FNAME placeholder>:
# # Need to establish the target macro names for the different test cases

# # Extra option for simulating cache
# .PHONY: build-sim-cache
# build-sim-cache: $(TARGET).elf
# #  --hartids=<a,b,...>   Explicitly specify hartids, default is 0,1,...
# #  --ic=<S>:<W>:<B>      Instantiate a cache model with S sets,
# #  --dc=<S>:<W>:<B>        W ways, and B-byte blocks (with S and
# #  --l2=<S>:<W>:<B>        B both powers of 2).
# #	DEFAULT lowRISC values
# #  --ic=64:4:8      Instantiate a cache model with S sets,
# #  --dc=64:4:8        W ways, and B-byte blocks (with S and
# #  --l2=256:8:8        B both powers of 2).
# 	@echo ""
# 	@echo "-------------  Build done, starting simulation  -------------"
# 	@$(SPIKE) -p$(N_PROC) --isa=$(ISA) --ic=64:4:8 --dc=64:4:8 --l2=256:8:8 $(TARGET).elf