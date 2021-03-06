.PHONY: dev
dev:
	poetry install

.PHONY: test
test:
	tox -e unit

.PHONY: coverage
coverage:
	tox -e coverage

.PHONY: submit_coverage
submit_coverage: coverage
	poetry run coveralls

.PHONY: install-hooks
install-hooks:
	tox -e install-hooks

.PHONY: release
release: clean
	python setup.py sdist bdist_wheel
	echo "Checking dist:"
	twine check dist/*
	# "Are you sure you want to publish the ^ release? Press any key to continue."
	read
	twine upload dist/*

.PHONY: acceptance
acceptance:
	poetry run tox -e acceptance

.PHONY: clean
clean:
	rm -rf build dist .coverage .mypy_cache .pytest_cache __pycache__ ntgen.egg-info .tox acceptance/*actual.txt
