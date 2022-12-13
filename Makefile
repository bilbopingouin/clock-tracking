.PHONY: test

test: syntax unittests


syntax:
	@echo "Checking the syntax..."
	@python3 -m flake8
	@echo "...done"

unittests:
	@echo "Running the unit tests..."
	@python3 -m coverage run -m pytest --capture=sys
	@echo "...done"

report:
	@python3 -m coverage report -m | grep -v dist-packages
