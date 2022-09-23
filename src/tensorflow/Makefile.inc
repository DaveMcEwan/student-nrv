# Makefile for TensorFlow Lite for Microcontrollers dependencies

#	General template
# Variable defining the location for the C++ file
# TEST_CC	 := ${SRC_TFLITE_KERNELS_DIR}/<File name>.cc
# Variable defining the location for the corresponding output object file
# TEST_OBJ := $(addsuffix /$(notdir $(subst .cc,.o,$(TEST_CC))),$(COMMON_DIRS))

# ${BUILD_DIR}/%/common/<File name>.o : ${SRC_TFLITE_KERNELS_DIR}/<File name>.cc
# 	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

#	FOLDERS
TFLITE_DIRS 				  := $(addsuffix tensorflow/lite/,${COMMON_DIRS})
TFLITE_C_DIRS 				  := $(addsuffix c/,${TFLITE_DIRS})
TFLITE_CORE_API_DIRS		  := $(addsuffix core/api/,${TFLITE_DIRS})
TFLITE_SCHEMA_DIRS			  := $(addsuffix schema/,${TFLITE_DIRS})
TFLITE_KERNELS_DIRS			  := $(addsuffix kernels/,${TFLITE_DIRS})
TFLITE_KERNELS_INTERNAL_DIRS  := $(addsuffix internal/,${TFLITE_KERNELS_DIRS})

TFLITE_MICRO_DIRS 			  := $(addsuffix micro/,${TFLITE_DIRS})
TFLITE_MICRO_AA_DIRS		  := $(addsuffix arena_allocator/,${TFLITE_MICRO_DIRS})
TFLITE_MICRO_MP_DIRS		  := $(addsuffix memory_planner/,${TFLITE_MICRO_DIRS})
TFLITE_MICRO_RISCV_DIRS		  := $(addsuffix riscv32_mcu/,${TFLITE_MICRO_DIRS})
TFLITE_MICRO_KERNELS_DIRS 	  := $(addsuffix kernels/,${TFLITE_MICRO_DIRS})

# Shortcuts to be used in directory names of targets
COMMON_TFLITE 				  := common/tensorflow/lite
COMMON_TFLITE_MICRO 		  := ${COMMON_TFLITE}/micro
COMMON_TFLITE_MICRO_KERNELS   := ${COMMON_TFLITE_MICRO}/kernels

#			--------------------- TFLITE TARGETS ---------------------
TFLITE_MICRO_SRCS := \
$(wildcard src/tensorflow/lite/micro/*.cc) \
$(wildcard src/tensorflow/lite/micro/arena_allocator/*.cc) \
$(wildcard src/tensorflow/lite/micro/memory_planner/*.cc) \
$(wildcard src/tensorflow/lite/micro/riscv32_mcu/*.cc)

# Written using secondary expansion so that the pattern rule can be accessed in
#	the dependency list for recipes
TFLITE_MICRO_OBJS := $$(subst .cc,.o,\
	$$(subst src/,$${BUILD_DIR}/$$*/../common/,$$(TFLITE_MICRO_SRCS)))

TFLITE_SRCS := \
$(wildcard src/tensorflow/lite/c/common.cc) \
$(wildcard src/tensorflow/lite/core/api/*.cc) \
$(wildcard src/tensorflow/lite/schema/*.cc) \
$(wildcard src/tensorflow/lite/kernels/*.cc) \
$(wildcard src/tensorflow/lite/kernels/internal/*.cc)

TFLITE_OBJS := $$(subst .cc,.o,\
	$$(subst src/,$${BUILD_DIR}/$$*/../common/,$$(TFLITE_SRCS)))

TFLITE_MICRO_KERNEL_SRCS := $(wildcard src/tensorflow/lite/micro/kernels/*.cc)

TFLITE_MICRO_KERNEL_OBJS := $$(subst .cc,.o,\
	$$(subst src/,$${BUILD_DIR}/$$*/../common/,$$(TFLITE_MICRO_KERNEL_SRCS)))

#	------------------------------ DIRECTORIES --------------------------------
# Targets to form all needed directories in one to avoid having multiple separate 
#	mkdir commands that flood the command line.
TFLITE_DIRS:
	mkdir -p ${TFLITE_DIRS}

TFLITE_C_DIRS:
	mkdir -p ${TFLITE_C_DIRS}

TFLITE_CORE_API_DIRS:
	mkdir -p ${TFLITE_CORE_API_DIRS}

TFLITE_SCHEMA_DIRS:
	mkdir -p ${TFLITE_SCHEMA_DIRS}

TFLITE_KERNELS_DIRS:
	mkdir -p ${TFLITE_KERNELS_DIRS}

TFLITE_KERNELS_INTERNAL_DIRS:
	mkdir -p ${TFLITE_KERNELS_INTERNAL_DIRS}

TFLITE_MICRO_DIRS:
	mkdir -p ${TFLITE_MICRO_DIRS}

TFLITE_MICRO_AA_DIRS:
	mkdir -p ${TFLITE_MICRO_AA_DIRS}

TFLITE_MICRO_MP_DIRS:
	mkdir -p ${TFLITE_MICRO_MP_DIRS}

TFLITE_MICRO_RISCV_DIRS:
	mkdir -p ${TFLITE_MICRO_RISCV_DIRS}

TFLITE_MICRO_KERNELS_DIRS:
	mkdir -p ${TFLITE_MICRO_KERNELS_DIRS}

# Multiple recipes needed due to the use of pattern detection

# GENERAL TFLITE FILES, TFLITE_OBJS
${BUILD_DIR}/%/${COMMON_TFLITE}/c/common.o : \
	${SRC_TFLITE_DIR}/c/common.cc \
	$(third_party_downloads) | TFLITE_C_DIRS
	
	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE}/core/api/error_reporter.o : \
	${SRC_TFLITE_DIR}/core/api/error_reporter.cc \
	$(third_party_downloads) | TFLITE_CORE_API_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE}/core/api/flatbuffer_conversions.o : \
	${SRC_TFLITE_DIR}/core/api/flatbuffer_conversions.cc \
	${FLATBUFFERS} | TFLITE_CORE_API_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE}/core/api/op_resolver.o : \
	${SRC_TFLITE_DIR}/core/api/op_resolver.cc \
	${FLATBUFFERS} | TFLITE_CORE_API_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE}/core/api/tensor_utils.o : \
	${SRC_TFLITE_DIR}/core/api/tensor_utils.cc \
	$(third_party_downloads) | TFLITE_CORE_API_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE}/schema/schema_utils.o : \
	${SRC_TFLITE_DIR}/schema/schema_utils.cc \
	${FLATBUFFERS} | TFLITE_SCHEMA_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE}/kernels/kernel_util.o : \
	${SRC_TFLITE_DIR}/kernels/kernel_util.cc \
	$(third_party_downloads) | TFLITE_KERNELS_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE}/kernels/internal/quantization_util.o : \
	${SRC_TFLITE_DIR}/kernels/internal/quantization_util.cc \
	$(third_party_downloads) | TFLITE_KERNELS_INTERNAL_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE}/kernels/internal/reference/portable_tensor_utils.o : \
	${SRC_TFLITE_DIR}/kernels/internal/reference/portable_tensor_utils.cc \
	$(third_party_downloads) | TFLITE_KERNELS_INTERNAL_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

# TFLITE MICRO FILES, TFLITE_MICRO_OBJS
${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/all_ops_resolver.o : \
	$(SRC_TFLITE_MICRO_DIR)/all_ops_resolver.cc \
	$(third_party_downloads) | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/fake_micro_context.o : \
	$(SRC_TFLITE_MICRO_DIR)/fake_micro_context.cc \
	$(third_party_downloads) | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/flatbuffer_utils.o : \
	$(SRC_TFLITE_MICRO_DIR)/flatbuffer_utils.cc \
	$(third_party_downloads) | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/memory_helpers.o : \
	$(SRC_TFLITE_MICRO_DIR)/memory_helpers.cc \
	${FLATBUFFERS} | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/micro_allocation_info.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_allocation_info.cc \
	$(third_party_downloads) | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/micro_allocator.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_allocator.cc \
	${FLATBUFFERS} | TFLITE_MICRO_DIRS
	
	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/micro_context.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_context.cc \
	$(third_party_downloads) | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/micro_error_reporter.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_error_reporter.cc \
	$(third_party_downloads) | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/micro_graph.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_graph.cc \
	${FLATBUFFERS} | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/micro_interpreter.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_interpreter.cc \
	${FLATBUFFERS} | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/micro_profiler.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_profiler.cc \
	$(third_party_downloads) | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/micro_resource_variable.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_resource_variable.cc \
	$(third_party_downloads) | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/micro_string.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_string.cc \
	$(third_party_downloads) | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/micro_time.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_time.cc \
	$(third_party_downloads) | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/micro_utils.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_utils.cc \
	$(third_party_downloads) | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/mock_micro_graph.o : \
	$(SRC_TFLITE_MICRO_DIR)/mock_micro_graph.cc \
	$(third_party_downloads) | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/recording_micro_allocator.o : \
	$(SRC_TFLITE_MICRO_DIR)/recording_micro_allocator.cc \
	$(third_party_downloads) | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/system_setup.o : \
	$(SRC_TFLITE_MICRO_DIR)/system_setup.cc \
	$(third_party_downloads) | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/test_helper_custom_ops.o : \
	$(SRC_TFLITE_MICRO_DIR)/test_helper_custom_ops.cc \
	${FLATBUFFERS} | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/test_helpers.o : \
	$(SRC_TFLITE_MICRO_DIR)/test_helpers.cc \
	${FLATBUFFERS} | TFLITE_MICRO_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/arena_allocator/non_persistent_arena_buffer_allocator.o : \
	$(SRC_TFLITE_MICRO_DIR)/arena_allocator/non_persistent_arena_buffer_allocator.cc \
	$(third_party_downloads) | TFLITE_MICRO_AA_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/arena_allocator/persistent_arena_buffer_allocator.o : \
	$(SRC_TFLITE_MICRO_DIR)/arena_allocator/persistent_arena_buffer_allocator.cc \
	$(third_party_downloads) | TFLITE_MICRO_AA_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/arena_allocator/recording_single_arena_buffer_allocator.o : \
	$(SRC_TFLITE_MICRO_DIR)/arena_allocator/recording_single_arena_buffer_allocator.cc \
	$(third_party_downloads) | TFLITE_MICRO_AA_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/arena_allocator/single_arena_buffer_allocator.o : \
	$(SRC_TFLITE_MICRO_DIR)/arena_allocator/single_arena_buffer_allocator.cc \
	$(third_party_downloads) | TFLITE_MICRO_AA_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/memory_planner/greedy_memory_planner.o : \
	$(SRC_TFLITE_MICRO_DIR)/memory_planner/greedy_memory_planner.cc \
	$(third_party_downloads) | TFLITE_MICRO_MP_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/memory_planner/linear_memory_planner.o : \
	$(SRC_TFLITE_MICRO_DIR)/memory_planner/linear_memory_planner.cc \
	$(third_party_downloads) | TFLITE_MICRO_MP_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/memory_planner/non_persistent_buffer_planner_shim.o : \
	$(SRC_TFLITE_MICRO_DIR)/memory_planner/non_persistent_buffer_planner_shim.cc \
	$(third_party_downloads) | TFLITE_MICRO_MP_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO}/riscv32_mcu/debug_log.o : \
	$(SRC_TFLITE_MICRO_DIR)/riscv32_mcu/debug_log.cc \
	$(third_party_downloads) | TFLITE_MICRO_RISCV_DIRS

	$(CC) $(CCFLAGS) ${CORE_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

# TFLITE MICRO KERNEL FILES, TFLITE_MICRO_KERNEL_OBJS
${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/activations_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/activations_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/activations.o : \
$(SRC_TFLITE_KERNELS_DIR)/activations.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/add_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/add_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/add_n.o : \
$(SRC_TFLITE_KERNELS_DIR)/add_n.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/add.o : \
$(SRC_TFLITE_KERNELS_DIR)/add.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/arg_min_max.o : \
$(SRC_TFLITE_KERNELS_DIR)/arg_min_max.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/assign_variable.o : \
$(SRC_TFLITE_KERNELS_DIR)/assign_variable.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/batch_to_space_nd.o : \
$(SRC_TFLITE_KERNELS_DIR)/batch_to_space_nd.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/broadcast_args.o : \
$(SRC_TFLITE_KERNELS_DIR)/broadcast_args.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/broadcast_to.o : \
$(SRC_TFLITE_KERNELS_DIR)/broadcast_to.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/call_once.o : \
$(SRC_TFLITE_KERNELS_DIR)/call_once.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/cast.o : \
$(SRC_TFLITE_KERNELS_DIR)/cast.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/ceil.o : \
$(SRC_TFLITE_KERNELS_DIR)/ceil.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/circular_buffer_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/circular_buffer_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/circular_buffer_flexbuffers_generated_data.o : \
$(SRC_TFLITE_KERNELS_DIR)/circular_buffer_flexbuffers_generated_data.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/circular_buffer.o : \
$(SRC_TFLITE_KERNELS_DIR)/circular_buffer.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/comparisons.o : \
$(SRC_TFLITE_KERNELS_DIR)/comparisons.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/concatenation.o : \
$(SRC_TFLITE_KERNELS_DIR)/concatenation.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/conv_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/conv_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/conv.o : \
$(SRC_TFLITE_KERNELS_DIR)/conv.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/cumsum.o : \
$(SRC_TFLITE_KERNELS_DIR)/cumsum.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/depth_to_space.o : \
$(SRC_TFLITE_KERNELS_DIR)/depth_to_space.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/depthwise_conv_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/depthwise_conv_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/depthwise_conv.o : \
$(SRC_TFLITE_KERNELS_DIR)/depthwise_conv.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/dequantize_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/dequantize_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/dequantize.o : \
$(SRC_TFLITE_KERNELS_DIR)/dequantize.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/detection_postprocess_flexbuffers_generated_data.o : \
$(SRC_TFLITE_KERNELS_DIR)/detection_postprocess_flexbuffers_generated_data.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/detection_postprocess.o : \
$(SRC_TFLITE_KERNELS_DIR)/detection_postprocess.cc \
	| TFLITE_MICRO_KERNELS_DIRS $(GEMMLOWP)
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/div.o : \
$(SRC_TFLITE_KERNELS_DIR)/div.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/elementwise.o : \
$(SRC_TFLITE_KERNELS_DIR)/elementwise.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/elu.o : \
$(SRC_TFLITE_KERNELS_DIR)/elu.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/ethosu.o : \
$(SRC_TFLITE_KERNELS_DIR)/ethosu.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/exp.o : \
$(SRC_TFLITE_KERNELS_DIR)/exp.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/expand_dims.o : \
$(SRC_TFLITE_KERNELS_DIR)/expand_dims.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/fill.o : \
$(SRC_TFLITE_KERNELS_DIR)/fill.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/floor_div.o : \
$(SRC_TFLITE_KERNELS_DIR)/floor_div.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/floor_mod.o : \
$(SRC_TFLITE_KERNELS_DIR)/floor_mod.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/floor.o : \
$(SRC_TFLITE_KERNELS_DIR)/floor.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/fully_connected_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/fully_connected_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/fully_connected.o : \
$(SRC_TFLITE_KERNELS_DIR)/fully_connected.cc \
 	| TFLITE_MICRO_KERNELS_DIRS $(RUYporting117DSn)
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/gather_nd.o : \
$(SRC_TFLITE_KERNELS_DIR)/gather_nd.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/gather.o : \
$(SRC_TFLITE_KERNELS_DIR)/gather.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/hard_swish_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/hard_swish_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/hard_swish.o : \
$(SRC_TFLITE_KERNELS_DIR)/hard_swish.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/if.o : \
$(SRC_TFLITE_KERNELS_DIR)/if.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/kernel_runner.o : \
$(SRC_TFLITE_KERNELS_DIR)/kernel_runner.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/kernel_util.o : \
$(SRC_TFLITE_KERNELS_DIR)/kernel_util.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/l2_pool_2d.o : \
$(SRC_TFLITE_KERNELS_DIR)/l2_pool_2d.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/l2norm.o : \
$(SRC_TFLITE_KERNELS_DIR)/l2norm.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/leaky_relu_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/leaky_relu_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/leaky_relu.o : \
$(SRC_TFLITE_KERNELS_DIR)/leaky_relu.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/log_softmax.o : \
$(SRC_TFLITE_KERNELS_DIR)/log_softmax.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/logical.o : \
$(SRC_TFLITE_KERNELS_DIR)/logical.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/logical_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/logical_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/logistic.o : \
$(SRC_TFLITE_KERNELS_DIR)/logistic.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/logistic_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/logistic_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/lstm_eval.o : \
$(SRC_TFLITE_KERNELS_DIR)/lstm_eval.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/maximum_minimum.o : \
$(SRC_TFLITE_KERNELS_DIR)/maximum_minimum.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/micro_tensor_utils.o : \
$(SRC_TFLITE_KERNELS_DIR)/micro_tensor_utils.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/mirror_pad.o : \
$(SRC_TFLITE_KERNELS_DIR)/mirror_pad.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/mul_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/mul_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/mul.o : \
$(SRC_TFLITE_KERNELS_DIR)/mul.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/neg.o : \
$(SRC_TFLITE_KERNELS_DIR)/neg.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/pack.o : \
$(SRC_TFLITE_KERNELS_DIR)/pack.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/pad.o : \
$(SRC_TFLITE_KERNELS_DIR)/pad.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/pooling_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/pooling_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/pooling.o : \
$(SRC_TFLITE_KERNELS_DIR)/pooling.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/prelu_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/prelu_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/prelu.o : \
$(SRC_TFLITE_KERNELS_DIR)/prelu.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/quantize_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/quantize_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/quantize.o : \
$(SRC_TFLITE_KERNELS_DIR)/quantize.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/read_variable.o : \
$(SRC_TFLITE_KERNELS_DIR)/read_variable.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/reduce_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/reduce_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/reduce.o : \
$(SRC_TFLITE_KERNELS_DIR)/reduce.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/reshape.o : \
$(SRC_TFLITE_KERNELS_DIR)/reshape.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/resize_bilinear.o : \
$(SRC_TFLITE_KERNELS_DIR)/resize_bilinear.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/resize_nearest_neighbor.o : \
$(SRC_TFLITE_KERNELS_DIR)/resize_nearest_neighbor.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/round.o : \
$(SRC_TFLITE_KERNELS_DIR)/round.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/select.o : \
$(SRC_TFLITE_KERNELS_DIR)/select.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/shape.o : \
$(SRC_TFLITE_KERNELS_DIR)/shape.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/slice.o : \
$(SRC_TFLITE_KERNELS_DIR)/slice.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/softmax_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/softmax_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/softmax.o : \
$(SRC_TFLITE_KERNELS_DIR)/softmax.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/space_to_batch_nd.o : \
$(SRC_TFLITE_KERNELS_DIR)/space_to_batch_nd.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/space_to_depth.o : \
$(SRC_TFLITE_KERNELS_DIR)/space_to_depth.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/split_v.o : \
$(SRC_TFLITE_KERNELS_DIR)/split_v.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/split.o : \
$(SRC_TFLITE_KERNELS_DIR)/split.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/squared_difference.o : \
$(SRC_TFLITE_KERNELS_DIR)/squared_difference.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/squeeze.o : \
$(SRC_TFLITE_KERNELS_DIR)/squeeze.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/strided_slice.o : \
$(SRC_TFLITE_KERNELS_DIR)/strided_slice.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/sub_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/sub_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/sub.o : \
$(SRC_TFLITE_KERNELS_DIR)/sub.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/svdf_common.o : \
$(SRC_TFLITE_KERNELS_DIR)/svdf_common.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/svdf.o : \
$(SRC_TFLITE_KERNELS_DIR)/svdf.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/tanh.o : \
$(SRC_TFLITE_KERNELS_DIR)/tanh.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/transpose_conv.o : \
$(SRC_TFLITE_KERNELS_DIR)/transpose_conv.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/transpose.o : \
$(SRC_TFLITE_KERNELS_DIR)/transpose.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/unidirectional_sequence_lstm.o : \
$(SRC_TFLITE_KERNELS_DIR)/unidirectional_sequence_lstm.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/unpack.o : \
$(SRC_TFLITE_KERNELS_DIR)/unpack.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/var_handle.o : \
$(SRC_TFLITE_KERNELS_DIR)/var_handle.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/while.o : \
$(SRC_TFLITE_KERNELS_DIR)/while.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@

${BUILD_DIR}/%/${COMMON_TFLITE_MICRO_KERNELS}/zeros_like.o : \
$(SRC_TFLITE_KERNELS_DIR)/zeros_like.cc \
$(third_party_downloads) | TFLITE_MICRO_KERNELS_DIRS
	$(CC) $(CCFLAGS) ${KERNEL_OPTIMIZATION_LEVEL} ${CC_INCLUDES} -c $< -o $@
