#******************************************************************************
#    Expanding upon the repo by Noureddine Ait Said : https://github.com/noureddine-as/riscv-baremetal-DefaultConfig
#------------------------------------------------------------------------------

.SECONDARY: # Used to stop make from deleting intermediate files

# default: build
# default: sim
default: disassembly
default: histogram
default: extract_main

# Macro definitions for directories to be used in the compile lines
SRC_DIR = ./src
SRC_OBJS_DIR = ./src/objs
CURRENT_DIR = .
BUILD_DIR = ./build

INCLUDES = -I./include

MK_CSV :=  ./csv/csv.mk
CSV ?= ./csv/config5.csv

# Checking if a CSV FNAME is set
ifndef CSV
$(shell echo There currently is no CSV FNAME set)
else
$(shell echo CSV FNAME currently set to : ${CSV})
endif

include ${MK_CSV}

# 	Label for a single target FNAME
# TODO : Adjust so that this isn't built around a single target
#	- One thing to note for the future, there are going to be multiple test cases per riscv test case configuration
#	- TARGET is the C source code we are building around; these are going to be placed in the subdirectories of /build
# TARGET = ${CURRENT_DIR}/baremetal-example
TEST_CASES = ./test_cases

# CSV and build directory forming
#	Variables
# R_XLEN = $(call CSV_VALUE_FIND, $*, 1)
# R_COMPILER = $(call CSV_VALUE_FIND, $*, 2)
# R_ISA = $(call CSV_VALUE_FIND, $*, 3)
# R_ABI = $(call CSV_VALUE_FIND, $*, 4)
# R_NPROC = $(call CSV_VALUE_FIND, $*, 5)
# R_FNAME = $(call CSV_VALUE_FIND, $*, 6)

comma:= ,
empty:=
dash := -
space:= $(empty) $(empty)

#	Folder name :	rv32gc-ilp32-gcc/simple_add
# This is input through the pattern rule and so we must break this down using $*
# https://www.gnu.org/software/make/manual/html_node/Text-Functions.html
# Using $shell
# COMPILER = $(shell echo $* | cut -d'-' -f3 | cut -d'/' -f1)
# ISA		 = $(shell echo $* | cut -d'-' -f1)
# XLEN 	 = $(findstring 32, ${ISA})
# XLEN 	 ?= $(findstring 64, ${ISA})
# ABI		 = $(shell echo $* | cut -d'-' -f2)
# FNAME    = $(shell echo $* | cut -d'/' -f2)

# Just using Makefile functions
DIRECTORY_NAME = $(subst $(dash),$(space),$*) # TODO - Rename into something more coherent
DIRECTORY_NAME_SPLIT = $(subst /,$(space), $(DIRECTORY_NAME))
ISA = $(word 1, $(DIRECTORY_NAME_SPLIT))
ABI = $(word 2, $(DIRECTORY_NAME_SPLIT))
COMPILER = $(word 3, $(DIRECTORY_NAME_SPLIT))
FNAME = $(word 4, $(DIRECTORY_NAME_SPLIT))
N_PROC = $(word 6, $(DIRECTORY_NAME_SPLIT))
XLEN 	 = $(findstring 32, ${ISA})
XLEN 	 ?= $(findstring 64, ${ISA})

CC = riscv$(XLEN)-unknown-elf-$(COMPILER)
# ISA = rv$(XLEN)$(ISA)

R_XLEN	= $(call CSV_COL,1,${row})
R_COMPILER	= $(call CSV_COL,2,${row})
R_ISA	= $(call CSV_COL,3,${row})
R_ABI	= $(call CSV_COL,4,${row})
R_NPROC = $(call CSV_COL,5,${row})
R_FNAME	= $(call CSV_COL,6,${row})

# CC = riscv$(R_XLEN)-unknown-elf-$(R_COMPILER)
# ISA = rv$(R_XLEN)$(R_ISA)

LINKER_SCRIPT = link.ld

# Parameter to determine how many processors to simulated when using Spike
# N_PROC ?= 4

# Checking if a RISCV compiler is present
ifndef RISCV
$(error "[ ERROR ] - RISCV variable not set!")
endif

OBJDUMP = $(RISCV)/bin/riscv$(XLEN)-unknown-elf-objdump
SIZE = $(RISCV)/bin/riscv$(XLEN)-unknown-elf-size
# LD = $(RISCV)/bin/riscv32-unknown-elf-ld # Using link flag with the default RISC-V compiler command
SPIKE = $(RISCV)/bin/spike

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

# Form the overall directory name
TRACES := $(foreach row,${CSV_ROWS},$\
	${BUILD_DIR}/$\
	rv$(call R_XLEN)$(call R_ISA)-$(call R_ABI)-$(call R_COMPILER)/$\
	$(call R_FNAME)/nproc-$(call R_NPROC)/instr-trace.trc)

# Strip down the directory name to grab the needed variables (can't get them directly from CSV rows)
# Note that these are lists of items, appending should be done using addsuffix to add to all items
NPROCDIRS := $(dir ${TRACES})
TESTDIRS := $(dir ${NPROCDIRS})
COMMON_ARCH := $(addsuffix ../common,${TESTDIRS})
# COMMON_ARCH := ${TESTDIRS}/../common # ${BUILD_DIR}/%/../common/
HISTOGRAMS := $(subst .trc,.hist,${TRACES})
OBJECTS := $(addsuffix testcase.o,${TRACES}) # ${BUILD_DIR}/%/testcase.o
EXECUTABLES := $(addsuffix testcase.elf,${TESTDIRS})
DISASSEMBLIES := $(subst .elf,.dasm,${EXECUTABLES})

# Variables

##### Can't grab variables in this way as this forms a list of variables which 
#####	is undesired since calling this in a recipe will just return the whole 
#####	list of variables. Accessing the specific one in a target requires 
#####	using the pattern rule.

# ARCHDIRS := ${TESTDIRS:./build/%/=%}
# FNAME := ${notdir ${ARCHDIRS}}
# STRIPPED_ARCHDIRS := $(dir ${ARCHDIRS})
# STRIPPED_ARCHDIRS := $(subst /, $(space), ${STRIPPED_ARCHDIRS}) 

# Need another way of grabbing the sections of STRIPPED_ARCHDIRS 
#	(since we need to consider that this is a whole list rather than just a single word)
# dash := -
# ISA = $(word 1,$(subst $(dash),$(space),${STRIPPED_ARCHDIRS}))
# XLEN = $(findstring 32, ${STRIPPED_ARCHDIRS})
# XLEN ?= $(findstring 64, ${STRIPPED_ARCHDIRS})
# # can use $(findstring)
# ABI = $(word 2,$(subst $(dash),$(space),${STRIPPED_ARCHDIRS}))
# COMPILER = $(word 3,$(subst $(dash),$(space),${STRIPPED_ARCHDIRS}))

# Can't grab the variables directly like this
# CC = riscv$(XLEN)-unknown-elf-$(COMPILER)
# ISA = rv$(call R_XLEN)$(call R_ISA)

test: TRACES
	@echo TRACES
	@echo ${TRACES}
	@echo
	@echo TESTDIRS
	@echo ${TESTDIRS}
	@echo
	@echo HISTOGRAMS
	@echo ${HISTOGRAMS}
	@echo
	@echo EXECUTABLES
	@echo ${EXECUTABLES}
	@echo
	@echo DISASSEMBLIES
	@echo ${DISASSEMBLIES}
	@echo
	@echo ARCHDIRS
	@echo ${ARCHDIRS}
	@echo
	@echo STRIPPED_ARCHDIRS
	@echo ${STRIPPED_ARCHDIRS}
	@echo
	@echo FNAME
	@echo ${FNAME}
	@echo
	@echo ISA
	@echo ${ISA}
	@echo
	@echo ABI
	@echo ${ABI}
	@echo
	@echo CC
	@echo ${CC}
	@echo
	@echo XLEN
	@echo ${XLEN}
	@echo

#	Testing
TRACES:
	mkdir -p $(TESTDIRS)
# ----------------------- BUILD -----------------------
# EXECUTABLES := $(addprefix ${BUILD_DIR}/,$(addsuffix /, $(CSV_ROWS))) 
# Target .elf files
# EXECUTABLES := $(addprefix ${BUILD_DIR}/,$(addsuffix /testcase.elf, $(CSV_ROWS))) #TODO - Break down
#	from CSV_ROWS

.PHONY: build
build: $(EXECUTABLES)
	@echo BUILD COMPLETE

# The rule to make $(EXECUTABLES)
# Output ELF
# ${BUILD_DIR}/%/testcase.elf - Need to have the target written like this (can't use EXECUTABLES)
# https://www.gnu.org/software/make/manual/html_node/Prerequisite-Types.html
$(BUILD_DIR)/%/testcase.elf: ${BUILD_DIR}/%/testcase.o $(BUILD_DIR)/%/../common/syscalls.o
	@echo --------- Linking into : testcase.elf ---------
	@echo $*
	$(CC) $^ ${SRC_DIR}/entry.S $(CFLAGS) ${INCLUDES} $(LDFLAGS) -o $@

# This is the first thing being done (bottom of the dependency tree) so we mkdir the directory here
$(BUILD_DIR)/%/testcase.o: ${SRC_DIR}/main.c # see if we can get the Make variable to be present in the dependency list
	@echo --------- Compiling into : testcase.o ---------
	@echo $(*)
	@echo ISA = $(ISA)
	@echo ABI = $(ABI)
	@echo COMPILER = $(COMPILER)
	@echo FNAME = $(FNAME)
	@echo XLEN = $(XLEN)
# mkdir -p $(addprefix ${BUILD_DIR}/,$(addsuffix /, $*))
	mkdir -p $(dir $@)
# mkdir -p ${TRACES}
	$(CC) $(CFLAGS) ${INCLUDES} -c ${TEST_CASES}/$(FNAME).c -o $@
# Producing the assembly FNAME for debugging
# $(CC) $(CFLAGS) ${INCLUDES} -S ${TEST_CASES}/$(FNAME).c -o ${BUILD_DIR}/$*/testcase.S
# TODO : Move assembly file creation to a different target

# Must be built within a specific directory because the compiled code is different in different architectures
# ${COMMON_ARCH}/syscalls.o
$(BUILD_DIR)/%/../common/syscalls.o: ${SRC_DIR}/syscalls.c
	@echo --------- Compiling into : syscalls.o ---------
#	mkdir -p $(addprefix ${BUILD_DIR}/,$(addsuffix /../common, $*))
	mkdir -p $(dir $@)
	$(CC) $(CFLAGS) ${INCLUDES} -w -c $< -o $@

# ----------------------- INSTRUCTION TRACE, DISASSEMBLY and HISTOGRAM -----------------------
# TRACES := $(addprefix ${BUILD_DIR}/,$(addsuffix /instruction-trace.log, $(CSV_ROWS))) 
# TRACES := $(foreach r,${CSV_ROWS},$\
# 	${BUILD}/$\
# 	rv$(call R_XLEN,$r)-$(call R_ABI,$r)-$(call R_COMPILER,$r)/$\
# 	$(call R_FNAME,$r)/nproc$(call R_NPROC,$r).trc)
.PHONY: sim
sim: $(TRACES)
	@echo SIMULATED

# ${BUILD_DIR}/%/instruction-trace.log

# $(addsuffix $(dir ${BUILD_DIR}/%), /testcase.elf)
${BUILD_DIR}/%/instr-trace.trc: ${BUILD_DIR}/%/../testcase.elf
	@echo --------- Simulation log printed to : ${BUILD_DIR}/$*/instruction-trace.log ---------
	@echo $(dir $(BUILD_DIR)/$*.trc)
	@echo $(DIRECTORY_NAME_SPLIT)
	$(SPIKE) -p$(N_PROC) -l --isa=$(ISA) $< 2> $@

# Choosing to separate the disassembly FNAME production from the simulation as someone may want to see the disassembly without simulating
# DISASSEMBLIES := $(addprefix ${BUILD_DIR}/,$(addsuffix /disassembly.dump, $(CSV_ROWS))) 
.PHONY: disassembly
disassembly: $(DISASSEMBLIES)

${BUILD_DIR}/%/disassembly.dump: ${BUILD_DIR}/%/testcase.elf
	@echo --------- Disassembly printed to : ${BUILD_DIR}/$*/disassembly.dump ---------
	$(OBJDUMP) -S -D $< > $@

# HISTOGRAMS := $(addprefix ${BUILD_DIR}/,$(addsuffix /histogram.txt, $(CSV_ROWS))) 
.PHONY: histogram
histogram: $(HISTOGRAMS)

${BUILD_DIR}/%/histogram.txt: ${BUILD_DIR}/%/testcase.elf
	@echo --------- Histogram printed to : $@ ---------
	$(SPIKE) -g --isa=$(ISA) $< 2> $@

EXTRACTED_MAIN_FILES := $(addprefix ${BUILD_DIR}/,$(addsuffix /main-instruction-trace.log, $(CSV_ROWS))) 
.PHONY: extract_main
extract_main: $(EXTRACTED_MAIN_FILES)

${BUILD_DIR}/%/main-instruction-trace.log : ${BUILD_DIR}/%/main-disassembly.dump ${BUILD_DIR}/%/instruction-trace.log
	@echo --------- Extracting the main instruction trace to : $@ ---------
	$(eval START_ADDRESS = $(shell cat $< | head -n1 | awk '{print $$1;}'))
	$(eval END_ADDRESS = $(shell cat $< | tail -n1 | awk '{print $$1;}' | tr -d ':'))
	sed -n '/$(START_ADDRESS)/,/$(END_ADDRESS)/p' ${BUILD_DIR}/$*/instruction-trace.log > $@

${BUILD_DIR}/%/main-disassembly.dump: ${BUILD_DIR}/%/disassembly.dump
	@echo --------- Extracting the main disassembly to : $@ ---------
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

# clean_sim:
# 	rm ${BUILD_DIR}/*/*.txt
# 	rm ${BUILD_DIR}/*/*.dump
# 	rm ${BUILD_DIR}/*/*.log