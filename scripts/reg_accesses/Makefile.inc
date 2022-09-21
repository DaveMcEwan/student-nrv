#		--------------------- REGISTER ACCESS TARGETS ---------------------
# Directories
REG_ACCESS_DIRS 	  := $(addsuffix reg_accesses/,${RESULT_DIRS})

# Target display files
# TODO : Adjust depending on the reg_display outputs
REG_ACCESS_DISPLAY	  := $(addsuffix counters_dist.pdf,${REG_ACCESS_DIRS})

# Target files
REG_ACCESS_COUNTERS   := $(addsuffix counters.JSON,${REG_ACCESS_DIRS})

# 				  -------------- REGISTER ACCESSES ---------------

.PHONY: display_reg_accesses
display_reg_accesses: ${REG_ACCESS_DISPLAY}

$(BUILD_DIR)/%/results/reg_accesses/counters_dist.pdf \
$(BUILD_DIR)/%/results/reg_accesses/counters_rs.pdf \
$(BUILD_DIR)/%/results/reg_accesses/counters_rd.pdf : \
	$$(addsuffix counters.JSON, $$(dir $$@))

	python3 scripts/reg_accesses/reg_display.py \
	-j=$< --img=$(addsuffix counters, $(dir $@))


.PHONY: reg_accesses
reg_accesses : ${REG_ACCESS_COUNTERS}

$(BUILD_DIR)/%/results/reg_accesses/counters.JSON : \
	$(BUILD_DIR)/%/main.trc

	mkdir -p $(dir $@)

	python3 scripts/reg_accesses/reg_accesses.py \
	--isa=${ISA} -j=$@ \
	< $< > $(subst .JSON,.txt,$@)