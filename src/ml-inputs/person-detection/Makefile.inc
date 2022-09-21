# Makefile for variables and dependencies specific to the person-detection ML input

#			--------------------- VARIABLES ---------------------
# SRC_PERSON_DETECTION_DIR - person-detection folder in the src/ml-inputs directory 
#	containing c++ files exclusive to the person-detection example
SRC_PRSN_DET_DIR := $(SRC_ML_DIR)/person-detection
# GEN_PERSON_DETECTION_DIR - person-detection folder located in the ml-input subdirectory
#	of each RISC-V configuration folder
GEN_PRSN_DET_DIR := $(GEN_ML_DIR)/person-detection

# PRSN_DET_DIRS	 	:=  $(addsuffix ../person-detection/,${FNAME_DIRS})
PRSN_DET_DEP_DIRS 	:=  $(addsuffix dependencies/,${FNAME_DIRS})

# PSRN_DET_TFLITE - .tflite file to extract the model data from
PRSN_DET_MODEL	 	:= $(SRC_PRSN_DET_DIR)/person_detect.tflite
PRSN_DET_MODEL_CC	:= ${GEN_PRSN_DET_DIR}/person_detect_model_data.cc
PRSN_DET_MODEL_H	:= ${GEN_PRSN_DET_DIR}/person_detect_model_data.h

# IMAGE DATA
#	PERSON IMAGE
PRSN_DET_P_BMP		:= 	$(SRC_PRSN_DET_DIR)/testdata/person.bmp
PRSN_DET_P_CC		:=	${GEN_PRSN_DET_DIR}/person_image_data.cc
PRSN_DET_P_H		:= 	${GEN_PRSN_DET_DIR}/person_image_data.h
# 	NO PERSON IMAGE
PRSN_DET_NP_BMP		:= 	$(SRC_PRSN_DET_DIR)/testdata/no_person.bmp
PRSN_DET_NP_CC		:=	${GEN_PRSN_DET_DIR}/no_person_image_data.cc
PRSN_DET_NP_H		:= 	${GEN_PRSN_DET_DIR}/no_person_image_data.h

person_detection_CC_FILES	:= \
$(wildcard ${SRC_PRSN_DET_DIR}/*.cc) \
$(wildcard ${SRC_PRSN_DET_DIR}/dependencies/*.cc) 

person_detection_O_FILES 	:= $$(subst .cc,.o,\
	$$(subst src/ml-inputs/person-detection/,$$(BUILD_DIR)/$$*/,$$(person_detection_CC_FILES)))

person_detection_GEN_CC_FILES	:= $(wildcard ${GEN_PRSN_DET_DIR}/*.cc)

person_detection_GEN_O_FILES := $$(subst .cc,.o,\
	$$(subst /ml-gen/person-detection/,/$$*/,$$(person_detection_GEN_CC_FILES)))

person_detection_O_FILES += $(person_detection_GEN_O_FILES)

#			--------------------- RECIPES ---------------------
# LIBRARY FILE
.SECONDEXPANSION:
$(BUILD_DIR)/%/person_detection.a: $(person_detection_O_FILES) | $(PRSN_DET_MODEL_CC) $(PRSN_DET_P_CC) $(PRSN_DET_NP_CC)
	@echo Making library file
	$(AR) -r $@ $^

# FOLDERS
PRSN_DET_DEP_DIRS:
	mkdir -p $(PRSN_DET_DEP_DIRS)

# MODEL DATA EXTRACTION
${PRSN_DET_MODEL_CC} ${PRSN_DET_MODEL_H} : ${PRSN_DET_MODEL}
	python3 tools/generate_cc_arrays.py $(dir $@) $<

# IMAGE DATA EXTRACTION
#	PERSON IMAGE
${PRSN_DET_P_CC} ${PRSN_DET_P_H} : ${PRSN_DET_P_BMP}
	python3 tools/generate_cc_arrays.py $(dir $@) $<
#	NO PERSON IMAGE
${PRSN_DET_NP_CC} ${PRSN_DET_NP_H} : ${PRSN_DET_NP_BMP}
	python3 tools/generate_cc_arrays.py $(dir $@) $<

# MODEL DATA
${BUILD_DIR}/%/person_detect_model_data.o: $(PRSN_DET_MODEL_CC) $(PRSN_DET_MODEL_H)
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

# IMAGE DATA
${BUILD_DIR}/%/person_image_data.o : ${PRSN_DET_P_CC}
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

${BUILD_DIR}/%/no_person_image_data.o : ${PRSN_DET_NP_CC}
	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

# MAIN
${BUILD_DIR}/%/person_detection_test.o : \
	${SRC_PRSN_DET_DIR}/person_detection_test.cc \
	| FNAME_DIRS ${PRSN_DET_MODEL_H} ${PRSN_DET_P_H} ${PRSN_DET_NP_H}

	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

# DEPENDENCIES
${BUILD_DIR}/%/dependencies/detection_responder.o : \
	${SRC_PRSN_DET_DIR}/dependencies/detection_responder.cc | PRSN_DET_DEP_DIRS

	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@

${BUILD_DIR}/%/dependencies/model_settings.o : \
	${SRC_PRSN_DET_DIR}/dependencies/model_settings.cc | PRSN_DET_DEP_DIRS

	$(CXX) $(CXXFLAGS) $(CORE_OPTIMIZATION_LEVEL) $(CXX_INCLUDES) -c $< -o $@
