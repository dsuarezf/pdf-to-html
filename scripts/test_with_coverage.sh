# Script to run unit tests with coverage

# Tests must be run from this folder
cd ../src

# Remove previous results
coverage erase

# Run tests with coverage
coverage run --source="main/python/." test/test.py

# Generate coverage report including only application under test
coverage report --include="main/python/*.py"

# Generate XML report for SonarQube
coverage xml -o test/cobertura.xml