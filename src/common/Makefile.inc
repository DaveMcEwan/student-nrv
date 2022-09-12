# Makefile for dependencies common throughout all ML programs

#	General template
# Variable defining the location for the C++ file
# TEST_CC	 := ${SRC_TFLITE_KERNELS_DIR}/<File name>.cc
# Variable defining the location for the corresponding output object file
# TEST_OBJ := $(addsuffix /$(notdir $(subst .cc,.o,$(TEST_CC))),$(COMMON_DIRS))

# $(BUILD_DIR)/%/common/<File name>.o : ${SRC_TFLITE_KERNELS_DIR}/<File name>.cc
# 	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

COMMON_TFLITE 				:= common/tensorflow/lite
COMMON_TFLITE_MICRO 		:= $(COMMON_TFLITE)/micro
COMMON_TFLITE_MICRO_KERNELS := $(COMMON_TFLITE_MICRO)/kernels

# GENERAL TFLITE FILES, TFLITE_LIB_OBJS
$(BUILD_DIR)/%/$(COMMON_TFLITE)/c/common.o : \
	$(SRC_TFLITE_DIR)/c/common.cc
	
	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE)/core/api/error_reporter.o : \
	$(SRC_TFLITE_DIR)/core/api/error_reporter.cc

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE)/core/api/flatbuffer_conversions.o : \
	$(SRC_TFLITE_DIR)/core/api/flatbuffer_conversions.cc \
	$(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE)/core/api/op_resolver.o : \
	$(SRC_TFLITE_DIR)/core/api/op_resolver.cc \
	$(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE)/core/api/tensor_utils.o : \
	$(SRC_TFLITE_DIR)/core/api/tensor_utils.cc

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE)/schema/schema_utils.o : \
	$(SRC_TFLITE_DIR)/schema/schema_utils.cc \
	$(FLATBUFFERS)
	
	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE)/kernels/kernel_util.o : \
	$(SRC_TFLITE_DIR)/kernels/kernel_util.cc

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE)/kernels/internal/quantization_util.o : \
	$(SRC_TFLITE_DIR)/kernels/internal/quantization_util.cc

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE)/kernels/internal/reference/portable_tensor_utils.o : \
	$(SRC_TFLITE_DIR)/kernels/internal/reference/portable_tensor_utils.cc

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

# TFLITE MICRO FILES, MICROLITE_LIB_OBJS
$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/all_ops_resolver.o : \
	$(SRC_TFLITE_MICRO_DIR)/all_ops_resolver.cc \
	$(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/fake_micro_context.o : \
	$(SRC_TFLITE_MICRO_DIR)/fake_micro_context.cc \
	$(FLATBUFFERS)

	mkdir -p $(dir $@)	
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/flatbuffer_utils.o : \
	$(SRC_TFLITE_MICRO_DIR)/flatbuffer_utils.cc \
	$(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/memory_helpers.o : \
	$(SRC_TFLITE_MICRO_DIR)/memory_helpers.cc \
	$(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/micro_allocation_info.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_allocation_info.cc \
	$(FLATBUFFERS)

	mkdir -p $(dir $@) 
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/micro_allocator.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_allocator.cc \
	$(FLATBUFFERS)

	mkdir -p $(dir $@)	
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/micro_context.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_context.cc \
	$(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/micro_error_reporter.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_error_reporter.cc

	mkdir -p $(dir $@) 
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/micro_graph.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_graph.cc \
	$(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/micro_interpreter.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_interpreter.cc \
	$(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/micro_profiler.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_profiler.cc

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/micro_resource_variable.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_resource_variable.cc \
	$(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/micro_string.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_string.cc

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/micro_time.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_time.cc

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/micro_utils.o : \
	$(SRC_TFLITE_MICRO_DIR)/micro_utils.cc \
	$(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/mock_micro_graph.o : \
	$(SRC_TFLITE_MICRO_DIR)/mock_micro_graph.cc \
	$(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/recording_micro_allocator.o : \
	$(SRC_TFLITE_MICRO_DIR)/recording_micro_allocator.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)	
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/system_setup.o : \
	$(SRC_TFLITE_MICRO_DIR)/system_setup.cc

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/test_helper_custom_ops.o : \
	$(SRC_TFLITE_MICRO_DIR)/test_helper_custom_ops.cc \
	$(FLATBUFFERS) 

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/test_helpers.o : \
	$(SRC_TFLITE_MICRO_DIR)/test_helpers.cc \
	$(FLATBUFFERS)
	
	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/arena_allocator/non_persistent_arena_buffer_allocator.o : \
	$(SRC_TFLITE_MICRO_DIR)/arena_allocator/non_persistent_arena_buffer_allocator.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/arena_allocator/persistent_arena_buffer_allocator.o : \
	$(SRC_TFLITE_MICRO_DIR)/arena_allocator/persistent_arena_buffer_allocator.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/arena_allocator/recording_single_arena_buffer_allocator.o : \
	$(SRC_TFLITE_MICRO_DIR)/arena_allocator/recording_single_arena_buffer_allocator.cc

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/arena_allocator/single_arena_buffer_allocator.o : \
	$(SRC_TFLITE_MICRO_DIR)/arena_allocator/single_arena_buffer_allocator.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/memory_planner/greedy_memory_planner.o : \
	$(SRC_TFLITE_MICRO_DIR)/memory_planner/greedy_memory_planner.cc \
	 | TFLITE_MICRO_MP_DIRS

	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/memory_planner/linear_memory_planner.o : \
	$(SRC_TFLITE_MICRO_DIR)/memory_planner/linear_memory_planner.cc

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/memory_planner/non_persistent_buffer_planner_shim.o : \
	$(SRC_TFLITE_MICRO_DIR)/memory_planner/non_persistent_buffer_planner_shim.cc

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO)/riscv32_mcu/debug_log.o : \
	$(SRC_TFLITE_MICRO_DIR)/riscv32_mcu/debug_log.cc

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

# TFLITE MICRO KERNEL FILES, MICROLITE_KERNEL_LIB_OBJS
$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/activations_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/activations_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/activations.o : \
	$(SRC_TFLITE_KERNELS_DIR)/activations.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/add_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/add_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/add_n.o : \
	$(SRC_TFLITE_KERNELS_DIR)/add_n.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/add.o : \
	$(SRC_TFLITE_KERNELS_DIR)/add.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/arg_min_max.o : \
	$(SRC_TFLITE_KERNELS_DIR)/arg_min_max.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/assign_variable.o : \
	$(SRC_TFLITE_KERNELS_DIR)/assign_variable.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/batch_to_space_nd.o : \
	$(SRC_TFLITE_KERNELS_DIR)/batch_to_space_nd.cc \
	$(RUY)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/broadcast_args.o : \
	$(SRC_TFLITE_KERNELS_DIR)/broadcast_args.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/broadcast_to.o : \
	$(SRC_TFLITE_KERNELS_DIR)/broadcast_to.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/call_once.o : \
	$(SRC_TFLITE_KERNELS_DIR)/call_once.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/cast.o : \
	$(SRC_TFLITE_KERNELS_DIR)/cast.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/ceil.o : \
	$(SRC_TFLITE_KERNELS_DIR)/ceil.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/circular_buffer_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/circular_buffer_common.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/circular_buffer_flexbuffers_generated_data.o : \
	$(SRC_TFLITE_KERNELS_DIR)/circular_buffer_flexbuffers_generated_data.cc

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/circular_buffer.o : \
	$(SRC_TFLITE_KERNELS_DIR)/circular_buffer.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/comparisons.o : \
	$(SRC_TFLITE_KERNELS_DIR)/comparisons.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/concatenation.o : \
	$(SRC_TFLITE_KERNELS_DIR)/concatenation.cc \
    $(GEMMLOWP)
	
	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/conv_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/conv_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/conv.o : \
	$(SRC_TFLITE_KERNELS_DIR)/conv.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/cumsum.o : \
	$(SRC_TFLITE_KERNELS_DIR)/cumsum.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/depth_to_space.o : \
	$(SRC_TFLITE_KERNELS_DIR)/depth_to_space.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/depthwise_conv_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/depthwise_conv_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/depthwise_conv.o : \
	$(SRC_TFLITE_KERNELS_DIR)/depthwise_conv.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/dequantize_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/dequantize_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/dequantize.o : \
	$(SRC_TFLITE_KERNELS_DIR)/dequantize.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/detection_postprocess_flexbuffers_generated_data.o : \
	$(SRC_TFLITE_KERNELS_DIR)/detection_postprocess_flexbuffers_generated_data.cc

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/detection_postprocess.o : \
	$(SRC_TFLITE_KERNELS_DIR)/detection_postprocess.cc \
    $(FLATBUFFERS) $(GEMMLOWP) 

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/div.o : \
	$(SRC_TFLITE_KERNELS_DIR)/div.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/elementwise.o : \
	$(SRC_TFLITE_KERNELS_DIR)/elementwise.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/elu.o : \
	$(SRC_TFLITE_KERNELS_DIR)/elu.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/ethosu.o : \
	$(SRC_TFLITE_KERNELS_DIR)/ethosu.cc

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/exp.o : \
	$(SRC_TFLITE_KERNELS_DIR)/exp.cc \
	$(RUY)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/expand_dims.o : \
	$(SRC_TFLITE_KERNELS_DIR)/expand_dims.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/fill.o : \
	$(SRC_TFLITE_KERNELS_DIR)/fill.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/floor_div.o : \
	$(SRC_TFLITE_KERNELS_DIR)/floor_div.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/floor_mod.o : \
	$(SRC_TFLITE_KERNELS_DIR)/floor_mod.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/floor.o : \
	$(SRC_TFLITE_KERNELS_DIR)/floor.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/fully_connected_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/fully_connected_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/fully_connected.o : \
$(SRC_TFLITE_KERNELS_DIR)/fully_connected.cc \
    $(GEMMLOWP) $(RUY)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/gather_nd.o : \
	$(SRC_TFLITE_KERNELS_DIR)/gather_nd.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/gather.o : \
	$(SRC_TFLITE_KERNELS_DIR)/gather.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/hard_swish_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/hard_swish_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/hard_swish.o : \
	$(SRC_TFLITE_KERNELS_DIR)/hard_swish.cc \
	$(RUY)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/if.o : \
	$(SRC_TFLITE_KERNELS_DIR)/if.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/kernel_runner.o : \
	$(SRC_TFLITE_KERNELS_DIR)/kernel_runner.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/kernel_util.o : \
	$(SRC_TFLITE_KERNELS_DIR)/kernel_util.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/l2_pool_2d.o : \
	$(SRC_TFLITE_KERNELS_DIR)/l2_pool_2d.cc  \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/l2norm.o : \
	$(SRC_TFLITE_KERNELS_DIR)/l2norm.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/leaky_relu_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/leaky_relu_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/leaky_relu.o : \
	$(SRC_TFLITE_KERNELS_DIR)/leaky_relu.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/log_softmax.o : \
	$(SRC_TFLITE_KERNELS_DIR)/log_softmax.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/logical.o : \
	$(SRC_TFLITE_KERNELS_DIR)/logical.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/logical_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/logical_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/logistic.o : \
	$(SRC_TFLITE_KERNELS_DIR)/logistic.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/logistic_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/logistic_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/lstm_eval.o : \
	$(SRC_TFLITE_KERNELS_DIR)/lstm_eval.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/maximum_minimum.o : \
	$(SRC_TFLITE_KERNELS_DIR)/maximum_minimum.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/micro_tensor_utils.o : \
	$(SRC_TFLITE_KERNELS_DIR)/micro_tensor_utils.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/mirror_pad.o : \
	$(SRC_TFLITE_KERNELS_DIR)/mirror_pad.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/mul_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/mul_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/mul.o : \
	$(SRC_TFLITE_KERNELS_DIR)/mul.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/neg.o : \
	$(SRC_TFLITE_KERNELS_DIR)/neg.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/pack.o : \
	$(SRC_TFLITE_KERNELS_DIR)/pack.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/pad.o : \
	$(SRC_TFLITE_KERNELS_DIR)/pad.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/pooling_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/pooling_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/pooling.o : \
	$(SRC_TFLITE_KERNELS_DIR)/pooling.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/prelu_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/prelu_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/prelu.o : \
	$(SRC_TFLITE_KERNELS_DIR)/prelu.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/quantize_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/quantize_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/quantize.o : \
	$(SRC_TFLITE_KERNELS_DIR)/quantize.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/read_variable.o : \
	$(SRC_TFLITE_KERNELS_DIR)/read_variable.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/reduce_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/reduce_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/reduce.o : \
	$(SRC_TFLITE_KERNELS_DIR)/reduce.cc \
	$(RUY)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/reshape.o : \
	$(SRC_TFLITE_KERNELS_DIR)/reshape.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/resize_bilinear.o : \
	$(SRC_TFLITE_KERNELS_DIR)/resize_bilinear.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/resize_nearest_neighbor.o : \
	$(SRC_TFLITE_KERNELS_DIR)/resize_nearest_neighbor.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/round.o : \
	$(SRC_TFLITE_KERNELS_DIR)/round.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/select.o : \
	$(SRC_TFLITE_KERNELS_DIR)/select.cc \
	$(RUY)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/shape.o : \
	$(SRC_TFLITE_KERNELS_DIR)/shape.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/slice.o : \
	$(SRC_TFLITE_KERNELS_DIR)/slice.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/softmax_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/softmax_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/softmax.o : \
	$(SRC_TFLITE_KERNELS_DIR)/softmax.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/space_to_batch_nd.o : \
	$(SRC_TFLITE_KERNELS_DIR)/space_to_batch_nd.cc \
	$(RUY)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/space_to_depth.o : \
	$(SRC_TFLITE_KERNELS_DIR)/space_to_depth.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)

	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/split_v.o : \
	$(SRC_TFLITE_KERNELS_DIR)/split_v.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/split.o : \
	$(SRC_TFLITE_KERNELS_DIR)/split.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/squared_difference.o : \
	$(SRC_TFLITE_KERNELS_DIR)/squared_difference.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/squeeze.o : \
	$(SRC_TFLITE_KERNELS_DIR)/squeeze.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/strided_slice.o : \
	$(SRC_TFLITE_KERNELS_DIR)/strided_slice.cc \
	$(RUY)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/sub_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/sub_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/sub.o : \
	$(SRC_TFLITE_KERNELS_DIR)/sub.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/svdf_common.o : \
	$(SRC_TFLITE_KERNELS_DIR)/svdf_common.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/svdf.o : \
	$(SRC_TFLITE_KERNELS_DIR)/svdf.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/tanh.o : \
	$(SRC_TFLITE_KERNELS_DIR)/tanh.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/transpose_conv.o : \
	$(SRC_TFLITE_KERNELS_DIR)/transpose_conv.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/transpose.o : \
	$(SRC_TFLITE_KERNELS_DIR)/transpose.cc \
    $(GEMMLOWP)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/unidirectional_sequence_lstm.o : \
	$(SRC_TFLITE_KERNELS_DIR)/unidirectional_sequence_lstm.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/unpack.o : \
	$(SRC_TFLITE_KERNELS_DIR)/unpack.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/var_handle.o : \
	$(SRC_TFLITE_KERNELS_DIR)/var_handle.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/while.o : \
	$(SRC_TFLITE_KERNELS_DIR)/while.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

$(BUILD_DIR)/%/$(COMMON_TFLITE_MICRO_KERNELS)/zeros_like.o : \
	$(SRC_TFLITE_KERNELS_DIR)/zeros_like.cc \
    $(FLATBUFFERS)

	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(KERNEL_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@
