#******************************************************************************
#    Expanding upon the repo by Noureddine Ait Said : 
#		https://github.com/noureddine-as/riscv-baremetal-DefaultConfig
#------------------------------------------------------------------------------

.SECONDARY: # Used to stop make from deleting intermediate files

default: third_party_downloads
# Default target purely for Github actions - used to verify if Spike simulation
#	completes correctly without logging anything (which takes up hours and
#	consumes a lot of space)
# default: sim-test

# Default targets are just the final ones (not including intermediate targets)
# default: assembly
default: disassembly
# default: histogram
default: extract_main
default: display_bandwidth
default: display_instruction_sequences
default: display_reg_accesses

# Checking if a RISCV compiler is present
ifndef RISCV
$(error "[ ERROR ] - RISCV variable not set!")
endif

# ------------------------ Variable definitions -------------------------

# 	Macro definitions for directories to be used in the compile lines
# /src - Contains input .c files
SRC_DIR 		= src
# /src/common - Contains shared files between inputs e.g. syscalls.c
SRC_COMMON_DIR  = $(SRC_DIR)/common
# /src/ml-inputs - Contains directories used for code to be compiled for each
#	ML input
SRC_ML_DIR		= $(SRC_DIR)/ml-inputs

SRC_TFLITE_DIR	= $(SRC_DIR)/tensorflow/lite

SRC_TFLITE_MICRO_DIR	= $(SRC_DIR)/tensorflow/lite/micro

SRC_TFLITE_KERNELS_DIR	= $(SRC_TFLITE_MICRO_DIR)/kernels

SRC_TFLITE_DOWNLOADS_DIR = $(SRC_TFLITE_MICRO_DIR)/downloads
# /build - Constructed directory used to store outputs from recipes including
#	executables, instruction traces, display pngs etc.
BUILD_DIR 		= build
# /tools - Folder containing python scripts needed to make intermediate files
TOOLS_DIR		= tools

LINKER_SCRIPT 	= link.ld

# Makefile functions and variables used to parse the input .csv file here
MK_CSV 			:= ./csv/csv.mk
# Input CSV file
CSV 			?= ./csv/config5.csv

$(shell echo CSV FNAME currently set to : ${CSV})

include ${MK_CSV}

# In this Makefile, there are two sets of variables detailing the information
#	from the CSV files:
#	- Variables read from the CSV - We initially directly read the information 
#	from the CSVs and store them in variables/lists prefixed with 'R_'. This
#	allows us to set up the recipe targets and have the CSV information present
#	in the file path which can be read from after.
#	- Variables read using the pattern rule - We can only access specific values
#	in the recipe of a target but taking the information from the file path which
#	we can access using the pattern rule. These variables parse the file path for
#	each specific target and use that information in the recipes as desired

# ----- Variables based on the CSV - Used for initial directory formatting -----
# 	Forms lists of the values in specific columns
# ISA instruction word size - 32 or 64
R_XLEN		= $(call CSV_COL,1,${row})
# Compiler - gcc or clang
R_COMPILER	= $(call CSV_COL,2,${row})
# ISA - String detailing the ISA following the RISC-V naming convention
R_ISA		= $(call CSV_COL,3,${row})
# ABI - Application binary interface : ilp32, lp64 or ilp32e
R_ABI		= $(call CSV_COL,4,${row})
# NPROC - How many cores we are using to simulate the program
R_NPROC 	= $(call CSV_COL,5,${row})
# FNAME - Input ML program name
R_FNAME		= $(call CSV_COL,6,${row})

# ---------------------------- Forming the targets ----------------------------
# Targets are created under directory paths formed by the information from the CSV files
#	collected in the variables prefixed with 'R_'

# TRACES is a list holding all instruction trace target directory paths which 
# 	will be used to form the other targets. Formed by looking at all rows of the CSV 
# 	e.g. build/rv32gc-ilp32-gcc/cv_testcase/nproc-8/whole.trc
#		 build/$(isa)-$(abi)-$(compiler)/$(fname)/whole.trc
TRACES := $(foreach row,${CSV_ROWS},$\
	${BUILD_DIR}/$\
	rv$(call R_XLEN)$(call R_ISA)-$(call R_ABI)-$(call R_COMPILER)/$\
	$(call R_FNAME)/nproc-$(call R_NPROC)/whole.trc)

# 	Form the other targets using string manipulation with the current target

# main.trc - Section of instruction trace between where we enter and leave main
MAIN_TRACES    := $(subst whole,main,${TRACES})
# test.txt - Stdout from purely simulating the input program without logging.
#	Used just to check if executables simulate properly without waiting hours
#	for the logging to complete.
TEST_TRACES	   := $(subst whole.trc,test.txt,${TRACES})

# 	Directory names - Formed by adjusting the TRACES list
# nproc - subdirectories used to contain the files associated with
#	simulating with a specific number of processors
#	e.g. build/rv32gc-ilp32-gcc/person_detection/nproc-1/
NPROC_DIRS 	:= $(dir ${TRACES})
# results - subdirectories for any results/diagrams
#	e.g. build/rv32gc-ilp32-gcc/person_detection/nproc-1/results
RESULT_DIRS := $(addsuffix results/,${NPROC_DIRS})
# fname - subdirectories holding all files related to a single input ML file
#	e.g. build/rv32gc-ilp32-gcc/person_detection/
FNAME_DIRS 	:= $(addsuffix ../,${NPROC_DIRS})
# common - subdirectory used to store temporary files used by multiple test cases
#	common to a single architecture configuration
#	e.g. build/rv32gc-ilp32-gcc/common/
COMMON_DIRS := $(addsuffix ../common/,${FNAME_DIRS})

#	Target files
# Executable to be passed through Spike
EXECUTABLES 	   := $(addsuffix executable.elf,${FNAME_DIRS})
DISASSEMBLIES	   := $(addsuffix disassembly.dasm,${FNAME_DIRS})
# (main) section of the disassembly
MAIN_DISASSEMBLIES := $(subst disassembly,main,${DISASSEMBLIES})

#			--------------------- ML TARGETS ---------------------
GEN_ML_DIR		:=	${BUILD_DIR}/ml-gen

# --------------- Variable definitions based on the pattern rule ---------------
# Second set of variable names/definitions. This one is formed based on the
#	pattern rule where the information is taken from the file path of the target.

# Example file path : rv32gc-ilp32-gcc/printf/nproc-2/

# Splitting up the file path into individual components
# $* - Pattern rule from which the file path will be determined from
DIRNAME_SPLIT1 = $(subst -,${space},$*)
DIRNAME_SPLIT2 = $(subst /,${space}, $(DIRNAME_SPLIT1))
# The example at this point would then be : rv32gc ilp32 gcc printf nproc 2
ISA 		= $(word 1, $(DIRNAME_SPLIT2)) # rv32gc
ABI			= $(word 2, $(DIRNAME_SPLIT2)) # ilp32
COMPILER 	= $(word 3, $(DIRNAME_SPLIT2)) # gcc
FNAME 		= $(word 4, $(DIRNAME_SPLIT2)) # printf
# The 5th word is nproc; no information we can take from this
N_PROC 		= $(word 6, $(DIRNAME_SPLIT2)) # 2

# If there is a '32' present in rv__, set XLEN to it. 
#	Else set it to 64 if that is present
XLEN 	 	= $(findstring 32, $(ISA))
XLEN 	 	?= $(findstring 64, $(ISA))

#	Commands used within recipes that require these variables taken from the
#		file path using the pattern rule
CC 		= riscv$(XLEN)-unknown-elf-$(COMPILER)	# Compilation command
OBJDUMP = ${RISCV}/bin/riscv$(XLEN)-unknown-elf-objdump
SIZE 	= ${RISCV}/bin/riscv$(XLEN)-unknown-elf-size
AR		= riscv$(XLEN)-unknown-elf-ar

# SPIKE 	= ${RISCV}/bin/spike
SPIKE	= spike

# ------------- Variables definitions based on the recipe target -------------
# $@ - Recipe target
WINDOW_SIZE = $(word 3, $(subst -, ,$(basename $(notdir $@))))

# -------------------------- Default compiler flags --------------------------
# More information : https://gcc.gnu.org/onlinedocs/gcc/RISC-V-Options.html

# ISA Configuration
#	- Determines the base instruction set and the additional extensions
#	- Uses:
#		- Spike - Determines what instructions and registers to have available
#		when simulating,
#		- Script analysis - Determines what instructions and registers to look
#		at when parsing.
CCFLAGS = -march=${ISA}

# ABI - Application Binary Interface
#	- Specifies the integer and floating-point calling convention
#	- Determines the bit sizes of the types
CCFLAGS += -mabi=${ABI}

# mcmodel -  Code model
#	- Determines the code model (medlow/medium-low or medany/medium-any)
#	- Used to determine conditions for the address range where the program
#	and it's statically defifned symbols can be placed
CCFLAGS += -mcmodel=medany

# freestanding program
#	- Tells the compiler that the standard library may not exist and so
#	it should be a freestanding/bare-metal program (does not load an external
#	module)
#	- Needed so that we can use functions provided by syscalls.c that use
#	the HTIF (Host/Target Interface) which the Spike simulator will be
#	able to simulate
CCFLAGS += -ffreestanding

# Static libraries
#	- Forces program to use static libraries
#	- Needed to allow us to specifically state what libraries we want present in
#	the program
CCFLAGS += -static
CCFLAGS += -lgcc

# No standard libraries
#	- Tells the program to not use the standard system startup files or libraries 
#	when linking
#	- Allows us to use our own linker scripts
CCFLAGS += -nostdlib

# No standard startup files
#	- Tells the compiler to not use the standard system startup files when linking
#	- Allows us to use our own startup files which work unlike the standard ones
#	in setting up the system so that it can be simulated in Spike properly.
CCFLAGS += -nostartfiles

CCFLAGS += \
	-std=c++11 \
	-fno-rtti \
	-fno-exceptions \
	-fno-threadsafe-statics \
	-fno-unwind-tables \
	-ffunction-sections \
	-fdata-sections \
	-fmessage-length=0 \
	-DTF_LITE_STATIC_MEMORY \
	-DTF_LITE_DISABLE_X86_NEON \
	-Wsign-compare \
	-Wshadow \
	-Wswitch \
	-Wvla \
	-Wextra \
	-Wmissing-field-initializers \
	-Wstrict-aliasing \
	-mexplicit-relocs \
	-fno-builtin-printf \
	-DTF_LITE_MCU_DEBUG_LOG \
	-DTF_LITE_USE_GLOBAL_CMATH_FUNCTIONS \
	-funsigned-char -fno-delete-null-pointer-checks \
	-fomit-frame-pointer \
	-fpermissive \
	-fno-use-cxa-atexit \
	-DTF_LITE_USE_GLOBAL_MIN \
	-DTF_LITE_USE_GLOBAL_MAX

CC_INCLUDES = -I. \
	-I$(SRC_TFLITE_DOWNLOADS_DIR)/gemmlowp \
	-I$(SRC_TFLITE_DOWNLOADS_DIR)/flatbuffers/include \
	-I$(SRC_TFLITE_DOWNLOADS_DIR)/ruy \
	-I./include \
	-I$(SRC_DIR) \
	-I${GEN_ML_DIR}

CORE_OPTIMIZATION_LEVEL = -Os
KERNEL_OPTIMIZATION_LEVEL = -O2


#	------------------------------ DIRECTORIES --------------------------------
# Targets to form all needed directories in one to avoid having multiple separate 
#	mkdir commands that flood the command line.

TRACES:
	mkdir -p ${FNAME_DIRS}

NPROC_DIRS:
	mkdir -p ${NPROC_DIRS}

FNAME_DIRS:
	mkdir -p ${FNAME_DIRS}

# .PHONY: COMMON_DIRS
COMMON_DIRS:
	mkdir -p ${COMMON_DIRS}

# .PHONY: RESULT_DIRS
RESULT_DIRS:
	mkdir -p ${RESULT_DIRS}

LOAD_BW_DIRS:
	mkdir -p ${LOAD_BW_DIRS}

STORE_BW_DIRS:
	mkdir -p ${STORE_BW_DIRS}

RAW_INSN_SEQ_DIRS:
	mkdir -p ${RAW_INSN_SEQ_DIRS}

FILTERED_INSN_SEQ_DIRS:
	mkdir -p ${FILTERED_INSN_SEQ_DIRS}

LIB_DIRS:
	mkdir -p ${LIB_DIRS}

SRC_TFLITE_DOWNLOADS_DIR:
	mkdir -p ${SRC_TFLITE_DOWNLOADS_DIR}

# --------------------------- THIRD PARTY DOWNLOADS  --------------------------
$(SRC_TFLITE_DOWNLOADS_DIR)/flatbuffers: SRC_TFLITE_DOWNLOADS_DIR
	$(TOOLS_DIR)/flatbuffers_download.sh $(SRC_TFLITE_DOWNLOADS_DIR)

$(SRC_TFLITE_DOWNLOADS_DIR)/kissfft: SRC_TFLITE_DOWNLOADS_DIR
	$(TOOLS_DIR)/kissfft_download.sh $(SRC_TFLITE_DOWNLOADS_DIR)

$(SRC_TFLITE_DOWNLOADS_DIR)/pigweed: SRC_TFLITE_DOWNLOADS_DIR
	$(TOOLS_DIR)/pigweed_download.sh $(SRC_TFLITE_DOWNLOADS_DIR)

GEMMLOWP_URL = "https://github.com/google/gemmlowp/archive/719139ce755a0f31cbf1c37f7f98adcc7fc9f425.zip"
GEMMLOWP_MD5 = "7e8191b24853d75de2af87622ad293ba"

$(SRC_TFLITE_DOWNLOADS_DIR)/gemmlowp: SRC_TFLITE_DOWNLOADS_DIR
	$(TOOLS_DIR)/download_and_extract.sh $(GEMMLOWP_URL) $(GEMMLOWP_MD5) $@

RUY_URL = "https://github.com/google/ruy/archive/d37128311b445e758136b8602d1bbd2a755e115d.zip"
RUY_MD5 = "abf7a91eb90d195f016ebe0be885bb6e"

$(SRC_TFLITE_DOWNLOADS_DIR)/ruy: SRC_TFLITE_DOWNLOADS_DIR
	$(TOOLS_DIR)/download_and_extract.sh $(RUY_URL) $(RUY_MD5) $@

.PHONY: third_party_downloads
third_party_downloads : $(SRC_TFLITE_DOWNLOADS_DIR)/flatbuffers \
$(SRC_TFLITE_DOWNLOADS_DIR)/kissfft \
$(SRC_TFLITE_DOWNLOADS_DIR)/pigweed \
$(SRC_TFLITE_DOWNLOADS_DIR)/gemmlowp \
$(SRC_TFLITE_DOWNLOADS_DIR)/ruy

# -------------------------------- GENERAL DEPENDENCIES --------------------------------
# Details of all recipes can be found in /doc/dependencies.md
# ----------------------------------- BUILD -----------------------------------
# Recipes for all of the default common TFLite 
include $(SRC_COMMON_DIR)/Makefile.inc
include $(SRC_DIR)/examples/printf.inc
include $(SRC_ML_DIR)/person-detection/Makefile.inc

.PHONY: build
build: ${EXECUTABLES}

# First dependency of this recipe is dependent on information in the file path of the
#	recipe which must be expanded into $*. Secondary expansion is used to then access
#	the file path through the pattern rule which after parsing a bit and adding the 
#	necessary prefixes and suffixes, forms the file path for the input test case (whose
#	name is present in the file path)
.SECONDEXPANSION:
$(BUILD_DIR)/%/executable.elf: \
	$(BUILD_DIR)/%/../common/syscalls.o \
	$(BUILD_DIR)/$$*/$$(word 2, $$(subst /, ,$$*)).a \
	$(MICROLITE_LIB_OBJS) $(TFLITE_LIB_OBJS) $(MICROLITE_KERNEL_LIB_OBJS) \
	${SRC_COMMON_DIR}/entry.S
	
	mkdir -p $(dir $@)
	$(CC) -march=$(ISA) -mabi=$(ABI) -Wl,--fatal-warnings -Wl,--gc-sections \
	-nostartfiles -lm -lgcc \
	$(CC_INCLUDES) -T$(LINKER_SCRIPT) \
	-o $@ $^

# syscalls object file
${BUILD_DIR}/%/../common/syscalls.o: ${SRC_COMMON_DIR}/syscalls.c
	mkdir -p $(dir $@)
	${CC} ${CC_INCLUDES} -I./include -w -c $< -o $@

# --------------- INSTRUCTION TRACE and DISASSEMBLY ---------------

# Debugging recipe - Verify if simulation completes without logging
#	the instruction trace
.PHONY: sim-test
sim-test: ${TEST_TRACES}

${BUILD_DIR}/%/test.txt: ${BUILD_DIR}/%/../executable.elf | NPROC_DIRS
	${SPIKE} -p${N_PROC} --isa=$(ISA) $< > $@

# Instruction trace
.PHONY: sim
sim: ${TRACES}

${BUILD_DIR}/%/whole.trc: ${BUILD_DIR}/%/../executable.elf | NPROC_DIRS
	${SPIKE} -p${N_PROC} -l --isa=$(ISA) $< 2> $@

# Disassembly
.PHONY: disassembly
disassembly: ${DISASSEMBLIES}

${BUILD_DIR}/%/disassembly.dasm: ${BUILD_DIR}/%/executable.elf | FNAME_DIRS
	${OBJDUMP} -S -D $< > $@

# Reduced instruction trace that only covers the region where we
#	enter and leave main
.PHONY: extract_main
extract_main: ${MAIN_TRACES}

${BUILD_DIR}/%/main.trc: ${BUILD_DIR}/%/../main.dasm ${BUILD_DIR}/%/whole.trc | NPROC_DIRS
	$(eval START_ADDRESS = $(shell cat $< | head -n1 | awk '{print $$1;}'))
	$(eval END_ADDRESS = $(shell cat $< | tail -n1 | awk '{print $$1;}' | tr -d ':'))
	sed -n '/${START_ADDRESS}/,/${END_ADDRESS}/p' ${BUILD_DIR}/$*/whole.trc > $@

# Reduced disassembly - only covering the main function to then parse the start and end
#	address from
${BUILD_DIR}/%/../main.dasm: ${BUILD_DIR}/%/../disassembly.dasm | NPROC_DIRS
	sed -n '/<main>:/,/ret/p' $< > $@

# ------------------------ INSTRUCTION TRACE ANALYSIS -------------------------
# 			------------------------ BANDWIDTH -------------------------
include scripts/bandwidth/Makefile.inc

# 			-------------- INSTRUCTION PATTERN DETECTION ---------------
include scripts/insn_patterns/Makefile.inc

# 				  -------------- REGISTER ACCESSES ---------------
include scripts/reg_accesses/Makefile.inc

# ----------------------------------- CLEAN ------------------------------------
.PHONY: clean
clean:
	rm -r $(BUILD_DIR)

.PHONY: clean_downloads
clean_downloads:
	rm -rf $(SRC_TFLITE_DOWNLOADS_DIR)

###################################################################################
# # Spike with GDB
# .PHONY: debug
# debug:
# 	@echo "-------------------  Starting Debugging  -------------------"
# 	@${SPIKE} -d -p${N_PROC} --isa=$(ISA) $(TARGET).elf

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
# 	@${SPIKE} -p${N_PROC} --isa=$(ISA) --ic=64:4:8 --dc=64:4:8 --l2=256:8:8 $(TARGET).elf