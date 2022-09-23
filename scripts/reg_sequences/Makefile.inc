# Makefile variables and recipes for register sequence detection scripts

#		----------------- VARIABLES -----------------
# Directories
REG_SEQ_DIRS 			:= $(addsuffix reg_sequences/,$(RESULT_DIRS))
REG_ONLY_DIRS			:= $(addsuffix reg_only/,$(REG_SEQ_DIRS))
INSN_REG_DIRS			:= $(addsuffix insn_reg/,$(REG_SEQ_DIRS))

RAW_REG_ONLY_DIRS 		:= $(addsuffix raw/,$(REG_ONLY_DIRS))
RAW_INSN_REG_DIRS 		:= $(addsuffix raw/,$(INSN_REG_DIRS))

FILT_REG_ONLY_DIRS 		:= $(addsuffix filtered/,${REG_ONLY_DIRS})
FILT_INSN_REG_DIRS 		:= $(addsuffix filtered/,${INSN_REG_DIRS})

# Target display files
FILT_REG_ONLY_PAIRS_HEATMAPS := $(addsuffix pairs-heatmap.pdf,${FILT_REG_ONLY_DIRS})
FILT_REG_ONLY_PAIRS_COL 	 := $(addsuffix pairs-column.pdf,${FILT_REG_ONLY_DIRS})
FILT_REG_ONLY_PATTERNS_COL   := $(addsuffix patterns-column.pdf,${FILT_REG_ONLY_DIRS})

FILT_INSN_REG_PAIRS_HEATMAPS := $(addsuffix pairs-heatmap.pdf,${FILT_INSN_REG_DIRS})
FILT_INSN_REG_PAIRS_COL 	 := $(addsuffix pairs-column.pdf,${FILT_INSN_REG_DIRS})
FILT_INSN_REG_PATTERNS_COL   := $(addsuffix patterns-column.pdf,${FILT_INSN_REG_DIRS})

# Target files
FILT_REG_ONLY_PAIRS		:= $(addsuffix pairs.txt,${FILT_REG_ONLY_DIRS})
FILT_REG_ONLY_PATTERNS	:= $(addsuffix patterns.txt,${FILT_REG_ONLY_DIRS})

FILT_INSN_REG_PAIRS		:= $(addsuffix pairs.txt,${FILT_INSN_REG_DIRS})
FILT_INSN_REG_PATTERNS	:= $(addsuffix patterns.txt,${FILT_INSN_REG_DIRS})

# ---------------------------------  RECIPES ----------------------------------
# Folders
RAW_REG_ONLY_DIRS:
	mkdir -p ${RAW_REG_ONLY_DIRS}

RAW_INSN_REG_DIRS:
	mkdir -p ${RAW_INSN_REG_DIRS}

FILT_REG_ONLY_DIRS:
	mkdir -p ${FILT_REG_ONLY_DIRS}

FILT_INSN_REG_DIRS:
	mkdir -p ${FILT_INSN_REG_DIRS}

# Runs all scripts available
.PHONY: display_register_sequences
display_register_sequences : \
display_reg_only_pairs_heatmap display_insn_reg_pairs_heatmap \
display_reg_only_pairs_column display_insn_reg_pairs_column\
display_reg_only_patterns_column display_insn_reg_patterns_column

.PHONY: display_reg_only_pairs_heatmap display_insn_reg_pairs_heatmap \
display_reg_only_pairs_column display_insn_reg_pairs_column\
display_reg_only_patterns_column display_insn_reg_patterns_column

# Display heatmap of register pairs and their associated counters
display_reg_only_pairs_heatmap : ${FILT_REG_ONLY_PAIRS_HEATMAPS}
${BUILD_DIR}/%/results/reg_sequences/reg_only/filtered/pairs-heatmap.pdf : \
	${BUILD_DIR}/%/results/reg_sequences/reg_only/filtered/pairs.JSON | FILT_REG_ONLY_DIRS

	python3 scripts/display/heatmap.py \
	-j=$< -p=reg_pairs -i=$@

# Display heatmap of (insn+register) pairs and their associated counters
display_insn_reg_pairs_heatmap : ${FILT_INSN_REG_PAIRS_HEATMAPS}
${BUILD_DIR}/%/results/reg_sequences/insn_reg/filtered/pairs-heatmap.pdf : \
	${BUILD_DIR}/%/results/reg_sequences/insn_reg/filtered/pairs.JSON | FILT_INSN_REG_DIRS

	python3 scripts/display/heatmap.py \
	-j=$< -p=reg_pairs -i=$@

# Display a column graph of the most frequent register pairs
display_reg_only_pairs_column : ${FILT_REG_ONLY_PAIRS_COL}
${BUILD_DIR}/%/results/reg_sequences/reg_only/filtered/pairs-column.pdf : \
	${BUILD_DIR}/%/results/reg_sequences/reg_only/filtered/pairs.JSON | FILT_REG_ONLY_DIRS

	python3 scripts/display/column.py \
	-j=$< -p=reg_pairs -i=$@

# Display a column graph of the most frequent (insn+register) pairs
display_insn_reg_pairs_column : ${FILT_INSN_REG_PAIRS_COL}
${BUILD_DIR}/%/results/reg_sequences/insn_reg/filtered/pairs-column.pdf : \
	${BUILD_DIR}/%/results/reg_sequences/insn_reg/filtered/pairs.JSON | FILT_INSN_REG_DIRS

	python3 scripts/display/column.py \
	-j=$< -p=reg_pairs -i=$@

# Display a column graph of the most frequent register patterns
display_reg_only_patterns_column : ${FILT_REG_ONLY_PATTERNS_COL}
${BUILD_DIR}/%/results/reg_sequences/reg_only/filtered/patterns-column.pdf : \
	${BUILD_DIR}/%/results/reg_sequences/reg_only/filtered/patterns.JSON | FILT_REG_ONLY_DIRS

	python3 scripts/display/column.py \
	-j=$< -p=reg_patterns -i=$@

# Display a column graph of the most frequen register patterns
display_insn_reg_patterns_column : ${FILT_INSN_REG_PATTERNS_COL}
${BUILD_DIR}/%/results/reg_sequences/insn_reg/filtered/patterns-column.pdf : \
	${BUILD_DIR}/%/results/reg_sequences/insn_reg/filtered/patterns.JSON | FILT_INSN_REG_DIRS

	python3 scripts/display/column.py \
	-j=$< -p=reg_patterns -i=$@

# Get the most frequent register pairs and patterns without displaying
.PHONY: register_sequences
register_sequences : reg_only_pairs insn_reg_pairs \
reg_only_patterns insn_reg_patterns

# Get the most frequent register pairs
.PHONY: reg_only_pairs
reg_only_pairs : ${FILT_REG_ONLY_PAIRS}

${BUILD_DIR}/%/results/reg_sequences/reg_only/filtered/pairs.JSON \
${BUILD_DIR}/%/results/reg_sequences/reg_only/filtered/pairs.txt : \
	${BUILD_DIR}/%/main.trc | FILT_REG_ONLY_DIRS RAW_REG_ONLY_DIRS

	python3 scripts/reg_sequences/reg_pairs.py \
	--isa=$(ISA) -j=$(subst .txt,.JSON,$@) \
	< $< > $(subst .JSON,.txt,$@)

# Get the most frequent (insn+register) pairs
.PHONY: insn_reg_pairs
insn_reg_pairs : ${FILT_INSN_REG_PAIRS}

${BUILD_DIR}/%/results/reg_sequences/insn_reg/filtered/pairs.JSON \
${BUILD_DIR}/%/results/reg_sequences/insn_reg/filtered/pairs.txt: \
	${BUILD_DIR}/%/main.trc | FILT_INSN_REG_DIRS RAW_INSN_REG_DIRS

	python3 scripts/reg_sequences/insn_reg_pairs.py \
	--isa=$(ISA) -j=$(subst .txt,.JSON,$@) \
	< $< > $(subst .JSON,.txt,$@)

# Get the most frequent register patterns
.PHONY: reg_only_patterns 
reg_only_patterns : ${FILT_REG_ONLY_PATTERNS}

${BUILD_DIR}/%/results/reg_sequences/reg_only/filtered/patterns.JSON \
${BUILD_DIR}/%/results/reg_sequences/reg_only/filtered/patterns.txt \
${BUILD_DIR}/%/results/reg_sequences/reg_only/raw/patterns.txt \
${BUILD_DIR}/%/results/reg_sequences/reg_only/raw/patterns.JSON : \
	${BUILD_DIR}/%/main.trc | FILT_REG_ONLY_DIRS RAW_REG_ONLY_DIRS

	python3 scripts/reg_sequences/reg_patterns.py \
	--isa=$(ISA) -j=$(subst .txt,.JSON,$@) \
	-r=$(abspath $(addsuffix ../raw/patterns,$(dir $@))) \
	< $< > $(subst .JSON,.txt,$@)

# Get the most frequent (insn+register) patterns
.PHONY: insn_reg_patterns 
insn_reg_patterns : ${FILT_INSN_REG_PATTERNS}

${BUILD_DIR}/%/results/reg_sequences/insn_reg/filtered/patterns.JSON \
${BUILD_DIR}/%/results/reg_sequences/insn_reg/filtered/patterns.txt \
${BUILD_DIR}/%/results/reg_sequences/insn_reg/raw/patterns.txt \
${BUILD_DIR}/%/results/reg_sequences/insn_reg/raw/patterns.JSON : \
	${BUILD_DIR}/%/main.trc | FILT_INSN_REG_DIRS RAW_INSN_REG_DIRS

	python3 scripts/reg_sequences/insn_reg_patterns.py \
	--isa=$(ISA) -j=$(subst .txt,.JSON,$@) \
	-r=$(abspath $(addsuffix ../raw/patterns,$(dir $@))) \
	< $< > $(subst .JSON,.txt,$@)
