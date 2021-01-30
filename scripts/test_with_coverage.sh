# Script to run unit tests with coverage

# Tests must be run from this folder
cd ..

# Remove previous results
coverage erase

# Run tests with coverage
coverage run --source="src/main/python/." src/test/test.py

# Generate coverage report including only application under test
coverage report --include="src/main/python/*.py"

# Generate XML report for SonarQube
coverage xml -o src/test/cobertura.xml