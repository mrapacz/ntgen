.PHONY: test
test:
	tox


.PHONY: install-hooks
install-hooks:
	tox -e install-hooks


.PHONY: clean
clean:
	rm -rf .coverage .mypy_cache .pytest_cache __pycache__ ntgen.egg-info .tox
