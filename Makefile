.PHONY: dev
dev:
	pip install -r requirements-dev.txt

.PHONY: test
test: dev
	tox -e unit

.PHONY: coverage
coverage: dev
	tox -e coverage

.PHONY: submit_coverage
submit_coverage: coverage
	coveralls

.PHONY: install-hooks
install-hooks: dev
	tox -e install-hooks


.PHONY: clean
clean:
	rm -rf build .coverage .mypy_cache .pytest_cache __pycache__ ntgen.egg-info .tox
