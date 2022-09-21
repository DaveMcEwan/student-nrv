#			--------------------- VARIABLES ---------------------
CC_FILE	:= $(SRC_DIR)/examples/printf.cc
O_FILE  := $$(subst .cc,.o,\
	$$(subst src/examples/,$$(BUILD_DIR)/$$*/,$$(CC_FILE)))

#			--------------------- RECIPES ---------------------
# LIBRARY FILE
.SECONDEXPANSION:
$(BUILD_DIR)/%/printf.a : $(O_FILE)
	@echo Reaching lib file
	mkdir -p $(dir $@)
	$(AR) -r $@ $^

# MAIN
$(BUILD_DIR)/%/printf.o : $(SRC_DIR)/examples/printf.cc
	mkdir -p $(dir $@)
	$(CC) $(CCFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CC_INCLUDES) -c $< -o $@