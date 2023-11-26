# Define variables
REQUIREMENTS_FILE = requirements.txt
MAIN_SCRIPT = src/main.py
PYCACHE_DIR = src/__pycache__

# Phony targets (targets that don't represent files)
.PHONY: init run clean

# Default target, run if no argument/target is specified
all: clean init run

# Install required dependencies
init: $(REQUIREMENTS_FILE)
	pip install -r $<

# Run main script
run: $(MAIN_SCRIPT)
	python $<

# Clean up generated bytecode files
clean:
	rm -rf $(PYCACHE_DIR)

# Remove all generated bytecode files and reinstall dependencies
reset: clean init

# Display help message
help:
	@echo "Available targets:"
	@echo "  init         - Install dependencies"
	@echo "  run          - Run the main script"
	@echo "  clean        - Clean up generated files"
	@echo "  reset        - Clean up generated files and reinstall dependencies"
	@echo "  help         - Display this help message"