# Makefile variables and recipes for instruction sequence detection scripts

#		----------------- VARIABLES -----------------
# Directories
INSN_SEQ_DIRS 			:= $(addsuffix insn_sequences/,${RESULT_DIRS})
RAW_INSN_SEQ_DIRS 		:= $(addsuffix raw/,${INSN_SEQ_DIRS})
FILTERED_INSN_SEQ_DIRS 	:= $(addsuffix filtered/,${INSN_SEQ_DIRS})

# Target display files
FILTERED_INSN_PAIRS_HEATMAPS := $(addsuffix pairs-heatmap.pdf,${FILTERED_INSN_SEQ_DIRS})
FILTERED_INSN_PAIRS_COL := $(addsuffix pairs-column.pdf,${FILTERED_INSN_SEQ_DIRS})
FILTERED_INSN_PATTERNS_COL := $(addsuffix patterns-column.pdf,${FILTERED_INSN_SEQ_DIRS})

# Target files
FILTERED_INSN_PAIRS		:= $(addsuffix pairs.txt,${FILTERED_INSN_SEQ_DIRS})
FILTERED_INSN_PATTERNS	:= $(addsuffix patterns.txt,${FILTERED_INSN_SEQ_DIRS})

# 			-------------- RECIPES ---------------
# Runs all scripts available
.PHONY: display_instruction_sequences
display_instruction_sequences : \
display_insn_pairs_heatmap display_insn_pairs_column display_insn_patterns_column

.PHONY: display_insn_pairs_heatmap display_insn_pairs_column display_insn_patterns_column
# Display heatmap of instruction pairs and their associated counters
display_insn_pairs_heatmap 	 : ${FILTERED_INSN_PAIRS_HEATMAPS}
${BUILD_DIR}/%/results/insn_sequences/filtered/pairs-heatmap.pdf : \
	${BUILD_DIR}/%/results/insn_sequences/filtered/pairs.JSON | FILTERED_INSN_SEQ_DIRS

	python3 scripts/display/heatmap.py \
	-j=$< -p=insn_pairs -i=$@

# Display a column graph of the most frequent instruction pairs
display_insn_pairs_column 	 : ${FILTERED_INSN_PAIRS_COL}
${BUILD_DIR}/%/results/insn_sequences/filtered/pairs-column.pdf : \
	${BUILD_DIR}/%/results/insn_sequences/filtered/pairs.JSON | FILTERED_INSN_SEQ_DIRS

	python3 scripts/display/column.py \
	-j=$< -p=insn_pairs -i=$@

# Display a column graph of the most frequen instruction patterns
display_insn_patterns_column : ${FILTERED_INSN_PATTERNS_COL}
${BUILD_DIR}/%/results/insn_sequences/filtered/patterns-column.pdf : \
	${BUILD_DIR}/%/results/insn_sequences/filtered/patterns.JSON | FILTERED_INSN_SEQ_DIRS

	python3 scripts/display/column.py \
	-j=$< -p=insn_patterns -i=$@

# Get the most frequent instruction pairs and patterns without displaying
.PHONY: instruction_sequences
instruction_sequences : instruction_pairs instruction_patterns

# Get the most frequent instruction pairs
.PHONY: instruction_pairs
instruction_pairs : ${FILTERED_INSN_PAIRS}

${BUILD_DIR}/%/results/insn_sequences/filtered/pairs.JSON \
${BUILD_DIR}/%/results/insn_sequences/filtered/pairs.txt \
${BUILD_DIR}/%/results/insn_sequences/raw/pairs.txt \
${BUILD_DIR}/%/results/insn_sequences/raw/pairs.JSON : \
	${BUILD_DIR}/%/main.trc | FILTERED_INSN_SEQ_DIRS RAW_INSN_SEQ_DIRS

	python3 scripts/insn_patterns/insn_pairs.py \
	-j=$(subst .txt,.JSON,$@) \
	-r=$(abspath $(addsuffix ../raw/pairs,$(dir $@))) \
	< $< > $(subst .JSON,.txt,$@)

# Get the most frequent instruction patterns
.PHONY: instruction_patterns 
instruction_patterns : ${FILTERED_INSN_PATTERNS}

${BUILD_DIR}/%/results/insn_sequences/filtered/patterns.JSON \
${BUILD_DIR}/%/results/insn_sequences/filtered/patterns.txt \
${BUILD_DIR}/%/results/insn_sequences/raw/patterns.txt \
${BUILD_DIR}/%/results/insn_sequences/raw/patterns.JSON : \
	${BUILD_DIR}/%/main.trc | FILTERED_INSN_SEQ_DIRS RAW_INSN_SEQ_DIRS

	python3 scripts/insn_patterns/insn_patterns.py \
	-j=$(subst .txt,.JSON,$@) \
	-r=$(abspath $(addsuffix ../raw/patterns,$(dir $@))) \
	< $< > $(subst .JSON,.txt,$@)
