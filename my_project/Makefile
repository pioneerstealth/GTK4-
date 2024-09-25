# Define the Python interpreter to use
PYTHON := python3

# Define the path to the main application
MAIN := src/main.py

# Define the CSS file to apply styles
STYLES := styles.css

# Default task: Run the application
run:
	@echo "Running GTK4 application..."
	$(PYTHON) $(MAIN)

# Install dependencies (if required)
install:
	@echo "Installing dependencies..."
	pip install PyGObject

# Lint the code
lint:
	@echo "Linting code with flake8..."
	flake8 src/*.py

# Format the code with Black
format:
	@echo "Formatting code with black..."
	black src/*.py

# Clean up build artifacts (if any)
clean:
	@echo "Cleaning up..."
	rm -rf __pycache__

# Phony targets to avoid conflicts with files
.PHONY: run install lint format clean
