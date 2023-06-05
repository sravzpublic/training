# Makefile
SHELL := /bin/bash
.PHONY: default
default: run
INCLUDE_DIR=./include
SOURCES := $(wildcard *.cpp)
run:
	g++ --std=c++17 -I$(INCLUDE_DIR) $(SOURCES)  -o ./dist/tutorial
	./dist/tutorial
