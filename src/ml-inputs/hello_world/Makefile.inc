# Example .inc file for input ML programs
#	This provides the variables and recipes associated with the example 
#	hello_world program (src/examples/hello_world.cc).
#	It also acts as a template which anyone looking to add a new input
#	program to the system.

#			--------------------- VARIABLES ---------------------
# Define associated source files and object files. Note that some programs 
#	may have more files such as person_detection which has bitmap files as
#	it's inputs to the Neural Network which must first be converted to C++
#	arrays before being used.

# Main file for hello_world
CC_FILE	:= $(SRC_ML_DIR)/hello_world/main.cc
# Object file formed through secondary expansion so that the target
#	filepath matches the recipe target's filepath (which in this case
#	is the filepath in which hello_world.a, the library file is located)
# e.g. build/rv32gc-ilp32-gcc/hello_world//hello_world-main.o
O_FILE  := $$(subst main.cc,hello_world-main.o,\
	$$(subst src/ml-inputs/hello_world/,$$(BUILD_DIR)/$$*/,$$(CC_FILE)))

# If there are sub-folders within either your source or object file directories,
#	make sure to include rules to mkdir -p them here and then add them as
#	an order-only dependency in the recipes

#			--------------------- RECIPES ---------------------
# LIBRARY FILE
# Collect all associated object files into a single library file with the
#	same name as that used in input.csv
.SECONDEXPANSION:
$(BUILD_DIR)/%/hello_world.a : $(O_FILE) | FNAME_DIRS
	$(AR) -r $@ $^

# ALL OBJECT FILE RECIPES
# main
$(BUILD_DIR)/%/hello_world-main.o : $(SRC_ML_DIR)/hello_world/main.cc | FNAME_DIRS
	$(CC) $(CCFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CC_INCLUDES) -c $< -o $@