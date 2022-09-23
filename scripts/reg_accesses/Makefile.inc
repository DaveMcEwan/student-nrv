# Makefile variables and recipes for register access analysis scripts

#		--------------------- REGISTER ACCESS TARGETS ---------------------
# Directories
REG_ACCESS_DIRS 	  := $(addsuffix reg_accesses/,${RESULT_DIRS})

# Target display files
REG_ACCESS_DISPLAY	  := $(addsuffix counters_dist.pdf,${REG_ACCESS_DIRS})
REG_ACCESS_DISPLAY_RS := $(addsuffix counters_rs.pdf,${REG_ACCESS_DIRS})
REG_ACCESS_DISPLAY_RD := $(addsuffix counters_rd.pdf,${REG_ACCESS_DIRS})

# Target files
REG_ACCESS_COUNTERS   := $(addsuffix counters.JSON,${REG_ACCESS_DIRS})

# 				  -------------- REGISTER ACCESSES ---------------
# Form all display scripts for register accesses
.PHONY: display_reg_accesses
display_reg_accesses: ${REG_ACCESS_DISPLAY}

$(BUILD_DIR)/%/results/reg_accesses/counters_dist.pdf \
$(BUILD_DIR)/%/results/reg_accesses/counters_rs.pdf \
$(BUILD_DIR)/%/results/reg_accesses/counters_rd.pdf : \
	$$(addsuffix counters.JSON, $$(dir $$@))

	python3 scripts/reg_accesses/reg_display.py \
	-j=$< --img=$(addsuffix counters, $(dir $@))

# Run the reg_accesses.py script which looks at how often registers are 
#	accesses as source and destination registes
.PHONY: reg_accesses
reg_accesses : ${REG_ACCESS_COUNTERS}

$(BUILD_DIR)/%/results/reg_accesses/counters.JSON : \
	$(BUILD_DIR)/%/main.trc

	mkdir -p $(dir $@)

	python3 scripts/reg_accesses/reg_accesses.py \
	--isa=${ISA} -j=$@ \
	< $< > $(subst .JSON,.txt,$@)