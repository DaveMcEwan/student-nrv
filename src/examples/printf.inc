#			--------------------- VARIABLES ---------------------
CC_FILE	:= $(SRC_DIR)/examples/printf.cc
O_FILE  := $$(subst .cc,.o,\
	$$(subst src/examples/,$$(BUILD_DIR)/$$*/,$$(CC_FILE)))

#			--------------------- RECIPES ---------------------
# LIBRARY FILE
.SECONDEXPANSION:
$(BUILD_DIR)/%/printf.a : $(O_FILE) | FNAME_DIRS
	$(AR) -r $@ $^

# MAIN
$(BUILD_DIR)/%/printf.o : $(SRC_DIR)/examples/printf.cc | FNAME_DIRS
	$(CC) $(CCFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CC_INCLUDES) -c $< -o $@