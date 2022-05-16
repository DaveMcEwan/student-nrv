
SRC := src
BUILD ?= build

default:

# https://www.gnu.org/software/make/manual/html_node/Prerequisite-Types.html
${BUILD}:
	mkdir -p ${BUILD}

.PHONY: clean
clean:
	rm -rf ${BUILD}


