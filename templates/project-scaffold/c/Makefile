# {{PROJECT_NAME}} — Makefile
CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -O2
DEBUG_FLAGS = -g -DDEBUG
BUILD_DIR = build
SRC_DIR = src
TEST_DIR = tests

SRCS = $(wildcard $(SRC_DIR)/*.c)
OBJS = $(patsubst $(SRC_DIR)/%.c, $(BUILD_DIR)/%.o, $(SRCS))
TARGET = $(BUILD_DIR)/main

.PHONY: all clean test debug

all: $(TARGET)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $^ -o $@

test: $(BUILD_DIR)
	$(CC) $(CFLAGS) $(TEST_DIR)/test_core.c $(filter-out $(BUILD_DIR)/main.o, $(OBJS)) -o $(BUILD_DIR)/test_core
	./$(BUILD_DIR)/test_core

debug: CFLAGS += $(DEBUG_FLAGS)
debug: clean all

clean:
	rm -rf $(BUILD_DIR)
