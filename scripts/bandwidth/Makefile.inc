#		--------------------- BANDWIDTH TARGETS ---------------------
# Directories
BW_DIRS 	  := $(addsuffix bw/,${RESULT_DIRS})
LOAD_BW_DIRS  := $(addsuffix load/,${BW_DIRS})
STORE_BW_DIRS := $(addsuffix store/,${BW_DIRS})

# Raw bandwidth streams
LOAD_BYTE_STREAMS  := $(addsuffix load-byte-stream.JSON,${LOAD_BW_DIRS})
STORE_BYTE_STREAMS := $(addsuffix store-byte-stream.JSON,${STORE_BW_DIRS})

# Figures and corresponding average traces
LOAD_BW_2		  := $(addsuffix load-bw-2.pdf,${LOAD_BW_DIRS})
LOAD_BW_2_TRC	  := $(addsuffix load-bw-2.JSON,${LOAD_BW_DIRS})

LOAD_BW_4		  := $(addsuffix load-bw-4.pdf,${LOAD_BW_DIRS})
LOAD_BW_4_TRC	  := $(addsuffix load-bw-4.JSON,${LOAD_BW_DIRS})

LOAD_BW_8		  := $(addsuffix load-bw-8.pdf,${LOAD_BW_DIRS})
LOAD_BW_8_TRC	  := $(addsuffix load-bw-8.JSON,${LOAD_BW_DIRS})

LOAD_BW_16	  	  := $(addsuffix load-bw-16.pdf,${LOAD_BW_DIRS})
LOAD_BW_16_TRC	  := $(addsuffix load-bw-16.JSON,${LOAD_BW_DIRS})

LOAD_BW_32	  	  := $(addsuffix load-bw-32.pdf,${LOAD_BW_DIRS})
LOAD_BW_32_TRC	  := $(addsuffix load-bw-32.JSON,${LOAD_BW_DIRS})

LOAD_BW_64	  	  := $(addsuffix load-bw-64.pdf,${LOAD_BW_DIRS})
LOAD_BW_64_TRC	  := $(addsuffix load-bw-64.JSON,${LOAD_BW_DIRS})

LOAD_BW_128	  	  := $(addsuffix load-bw-128.pdf,${LOAD_BW_DIRS})
LOAD_BW_128_TRC	  := $(addsuffix load-bw-128.JSON,${LOAD_BW_DIRS})

LOAD_BW_32768	  := $(addsuffix load-bw-32768.pdf,${LOAD_BW_DIRS})
LOAD_BW_32768_TRC := $(addsuffix load-bw-32768.JSON,${LOAD_BW_DIRS})

STORE_BW_2		  := $(addsuffix store-bw-2.pdf,${STORE_BW_DIRS})
STORE_BW_2_TRC	  := $(addsuffix store-bw-2.JSON,${STORE_BW_DIRS})

STORE_BW_4		  := $(addsuffix store-bw-4.pdf,${STORE_BW_DIRS})
STORE_BW_4_TRC	  := $(addsuffix store-bw-4.JSON,${STORE_BW_DIRS})

STORE_BW_8		  := $(addsuffix store-bw-8.pdf,${STORE_BW_DIRS})
STORE_BW_8_TRC	  := $(addsuffix store-bw-8.JSON,${STORE_BW_DIRS})

STORE_BW_16	  	  := $(addsuffix store-bw-16.pdf,${STORE_BW_DIRS})
STORE_BW_16_TRC	  := $(addsuffix store-bw-16.JSON,${STORE_BW_DIRS})

STORE_BW_32	  	  := $(addsuffix store-bw-32.pdf,${STORE_BW_DIRS})
STORE_BW_32_TRC	  := $(addsuffix store-bw-32.JSON,${STORE_BW_DIRS})

STORE_BW_64	  	  := $(addsuffix store-bw-64.pdf,${STORE_BW_DIRS})
STORE_BW_64_TRC	  := $(addsuffix store-bw-64.JSON,${STORE_BW_DIRS})

STORE_BW_128	  := $(addsuffix store-bw-128.pdf,${STORE_BW_DIRS})
STORE_BW_128_TRC  := $(addsuffix store-bw-128.JSON,${STORE_BW_DIRS})

STORE_BW_32768	   := $(addsuffix store-bw-32768.pdf,${STORE_BW_DIRS})
STORE_BW_32768_TRC := $(addsuffix store-bw-32768.JSON,${STORE_BW_DIRS})

# 			------------------------ BANDWIDTH -------------------------
# make bandwidth - forms all possible figures
.PHONY: display_bandwidth
display_bandwidth: avg_load_bw_all avg_store_bw_all \
display_load_bw_all display_store_bw_all

# 			   ----------------------- LOAD ------------------------
# Display all
.PHONY: display_load_bw_all
display_load_bw_all	: $(LOAD_BW_2) $(LOAD_BW_4) $(LOAD_BW_8) \
${LOAD_BW_16} ${LOAD_BW_32} ${LOAD_BW_64} ${LOAD_BW_128} ${LOAD_BW_32768}

# Individual load targets for displaying
.PHONY: display_load_bw_2 display_load_bw_4 display_load_bw_8
.PHONY: display_load_bw_16 display_load_bw_32 display_load_bw_64
.PHONY: display_load_bw_128 display_load_bw_32768
display_load_bw_2 	: ${LOAD_BW_2}
display_load_bw_4 	: ${LOAD_BW_4}
display_load_bw_8 	: ${LOAD_BW_8}
display_load_bw_16 	: ${LOAD_BW_16}
display_load_bw_32 	: ${LOAD_BW_32}
display_load_bw_64 	: ${LOAD_BW_64}
display_load_bw_128 : ${LOAD_BW_128}
display_load_bw_32768 : ${LOAD_BW_32768}

# Grouped load targets
.PHONY: display_load_bw_small display_load_bw_medium \
display_load_bw_load display_load_bw_very_large
display_load_bw_small  : ${LOAD_BW_2} ${LOAD_BW_4}
display_load_bw_medium : ${LOAD_BW_8} ${LOAD_BW_16} ${LOAD_BW_32}
display_load_bw_large  : ${LOAD_BW_64} ${LOAD_BW_128}
display_load_bw_very_large : ${LOAD_BW_32768}

# Target 	 :	bw/load/load-bw-n.pdf = LOAD_BW_N
# Dependency :  bw/load/load-bw-n.trc = LOAD_BW_N_TRC
.SECONDEXPANSION:
${LOAD_BW_2} ${LOAD_BW_4} ${LOAD_BW_8} ${LOAD_BW_16} \
${LOAD_BW_32} ${LOAD_BW_64} ${LOAD_BW_128} ${LOAD_BW_32768} \
	: $$(subst .pdf,.JSON,$$@) | LOAD_BW_DIRS

	python3 scripts/display/line_graph.py -p=mov_avg \
	-l=$(addsuffix ../length.txt, $(dir $@)) \
	-n=$(WINDOW_SIZE) --img=$@ < $<

.PHONY: avg_load_bw_all
avg_load_bw_all : ${LOAD_BW_2_TRC} ${LOAD_BW_4_TRC} ${LOAD_BW_8_TRC} \
${LOAD_BW_16_TRC} ${LOAD_BW_32_TRC} ${LOAD_BW_64_TRC} ${LOAD_BW_128_TRC} \
${LOAD_BW_32768_TRC}

# Individual load targets for average trace calculations
.PHONY: avg_load_bw_2 avg_load_bw_4 avg_load_bw_8
.PHONY: avg_load_bw_16 avg_load_bw_32 avg_load_bw_64
.PHONY: avg_load_bw_128 avg_load_bw_32768
avg_load_bw_2 	: ${LOAD_BW_2_TRC}
avg_load_bw_4 	: ${LOAD_BW_4_TRC}
avg_load_bw_8 	: ${LOAD_BW_8_TRC}
avg_load_bw_16 	: ${LOAD_BW_16_TRC}
avg_load_bw_32 	: ${LOAD_BW_32_TRC}
avg_load_bw_64 	: ${LOAD_BW_64_TRC}
avg_load_bw_128 : ${LOAD_BW_128_TRC}
avg_load_bw_32768 : ${LOAD_BW_32768_TRC}

# Grouped load targets
.PHONY: avg_load_bw_small avg_load_bw_medium \
avg_load_bw_load avg_load_bw_very_large
avg_load_bw_small  : ${LOAD_BW_2_TRC} ${LOAD_BW_4_TRC}
avg_load_bw_medium : ${LOAD_BW_8_TRC} ${LOAD_BW_16_TRC} ${LOAD_BW_32_TRC}
avg_load_bw_large  : ${LOAD_BW_64_TRC} ${LOAD_BW_128_TRC}
avg_load_bw_very_large : ${LOAD_BW_32768_TRC}

# Target 	 :	bw/load/load-bw-n.trc = LOAD_BW_N_TRC
# Dependency :  bw/load/load-byte-stream.trc = LOAD_BYTE_STREAMS
.SECONDEXPANSION:
${LOAD_BW_2_TRC} ${LOAD_BW_4_TRC} ${LOAD_BW_8_TRC} ${LOAD_BW_16_TRC} \
${LOAD_BW_32_TRC} ${LOAD_BW_64_TRC} ${LOAD_BW_128_TRC} ${LOAD_BW_32768_TRC} \
	: $$(addsuffix load-byte-stream.JSON, $$(dir $$@)) | LOAD_BW_DIRS
	
	python3 scripts/common/moving_average.py \
	-n=$(WINDOW_SIZE) -j=$@ \
	-l=$(addsuffix ../length.txt, $(dir $@)) \
	< $<

# 			  ------------------------ STORE ------------------------
# Display all
.PHONY: display_store_bw_all
display_store_bw_all	: $(STORE_BW_2) $(STORE_BW_4) $(STORE_BW_8) \
${STORE_BW_16} ${STORE_BW_32} ${STORE_BW_64} ${STORE_BW_128} ${STORE_BW_32768}

# Individual store targets for displaying
.PHONY: display_store_bw_2 display_store_bw_4 display_store_bw_8
.PHONY: display_store_bw_16 display_store_bw_32 display_store_bw_64
.PHONY: display_store_bw_128 display_store_bw_32768
display_store_bw_2 	 : ${STORE_BW_2}
display_store_bw_4 	 : ${STORE_BW_4}
display_store_bw_8 	 : ${STORE_BW_8}
display_store_bw_16  : ${STORE_BW_16}
display_store_bw_32  : ${STORE_BW_32}
display_store_bw_64  : ${STORE_BW_64}
display_store_bw_128 : ${STORE_BW_128}
display_store_bw_32768 : ${STORE_BW_32768}

# Grouped store targets
.PHONY: display_store_bw_small display_store_bw_medium \
display_store_bw_store display_store_bw_very_large 
display_store_bw_small  : ${STORE_BW_2} ${STORE_BW_4}
display_store_bw_medium : ${STORE_BW_8} ${STORE_BW_16} ${STORE_BW_32}
display_store_bw_large  : ${STORE_BW_64} ${STORE_BW_128}
display_store_bw_very_large : ${STORE_BW_32768}

.SECONDEXPANSION:
${STORE_BW_2} ${STORE_BW_4} ${STORE_BW_8} ${STORE_BW_16} \
${STORE_BW_32} ${STORE_BW_64} ${STORE_BW_128} ${STORE_BW_32768} \
	: $$(addsuffix .JSON, $$(basename $$@)) | STORE_BW_DIRS

	python3 scripts/display/line_graph.py -p=mov_avg \
	-l=$(addsuffix ../length.txt, $(dir $@)) \
	-n=$(WINDOW_SIZE) --img=$@ < $<

.PHONY: avg_store_bw_all
avg_store_bw_all : ${STORE_BW_2_TRC} ${STORE_BW_4_TRC} ${STORE_BW_8_TRC} \
${STORE_BW_16_TRC} ${STORE_BW_32_TRC} ${STORE_BW_64_TRC} ${STORE_BW_128_TRC} \
${STORE_BW_32768_TRC}

# Individual store targets for average trace calculations
.PHONY: avg_store_bw_2 avg_store_bw_4 avg_store_bw_8
.PHONY: avg_store_bw_16 avg_store_bw_32 avg_store_bw_64
.PHONY: avg_store_bw_128
avg_store_bw_2 	 : ${STORE_BW_2_TRC}
avg_store_bw_4 	 : ${STORE_BW_4_TRC}
avg_store_bw_8 	 : ${STORE_BW_8_TRC}
avg_store_bw_16  : ${STORE_BW_16_TRC}
avg_store_bw_32  : ${STORE_BW_32_TRC}
avg_store_bw_64  : ${STORE_BW_64_TRC}
avg_store_bw_128 : ${STORE_BW_128_TRC}
avg_store_bw_32768 : ${STORE_BW_32768}

# Grouped store targets
.PHONY: avg_store_bw_small avg_store_bw_medium avg_store_bw_store
avg_store_bw_small  : ${STORE_BW_2_TRC} ${STORE_BW_4_TRC}
avg_store_bw_medium : ${STORE_BW_8_TRC} ${STORE_BW_16_TRC} ${STORE_BW_32_TRC}
avg_store_bw_large  : ${STORE_BW_64_TRC} ${STORE_BW_128_TRC}
avg_store_bw_very_large : ${STORE_BW_32768_TRC}

.SECONDEXPANSION:
${STORE_BW_2_TRC} ${STORE_BW_4_TRC} ${STORE_BW_8_TRC} ${STORE_BW_16_TRC} \
${STORE_BW_32_TRC} ${STORE_BW_64_TRC} ${STORE_BW_128_TRC} ${STORE_BW_32768_TRC} \
	: $$(addsuffix store-byte-stream.JSON, $$(dir $$@))
	
	mkdir -p $(dir $@)
	python3 scripts/common/moving_average.py \
	-n=$(WINDOW_SIZE) -j=$@ \
	-l=$(addsuffix ../length.txt, $(dir $@)) \
	< $<

# 	Recipes for solely producing the bandwidth streams
# make bandwidth_streams - forms all possible bandwidth stream traces
.PHONY: bandwidth_streams
bandwidth_streams: load_bw_streams store_bw_streams

.PHONY: load_bw_streams
load_bw_streams: ${LOAD_BYTE_STREAMS}
${BUILD_DIR}/%/results/bw/load/load-byte-stream.JSON : \
	${BUILD_DIR}/%/main.trc

	mkdir -p $(dir $@)
	python3 scripts/common/key_stream.py \
	-k=Ld -j=$@ \
	--isa=$(ISA) < $<

.PHONY: store_bw_streams
store_bw_streams: ${STORE_BYTE_STREAMS}
${BUILD_DIR}/%/results/bw/store/store-byte-stream.JSON : \
	${BUILD_DIR}/%/main.trc

	mkdir -p $(dir $@)
	python3 scripts/common/key_stream.py \
	-k=St -j=$@ \
	--isa=$(ISA) < $<