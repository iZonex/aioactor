all: test

.install-deps: $(shell find requirements -type f)
	@pip install -U -r requirements/dev.txt
	@touch .install-deps

isort:
	isort -rc aioactor
	isort -rc tests
	isort -rc examples

flake: .flake

.flake: .install-deps $(shell find aioactor -type f) \
                      $(shell find tests -type f) \
                      $(shell find examples -type f)
	@flake8 aioactor examples tests
	python setup.py check -rms
	@if ! isort -c -rc aioactor tests examples; then \
            echo "Import sort errors, run 'make isort' to fix them!!!"; \
            isort --diff -rc aioactor tests examples; \
            false; \
	fi
	@touch .flake

check_changes:
	@./tools/check_changes.py

.develop: .install-deps $(shell find aioactor -type f) .flake check_changes
	@pip install -e .
	@touch .develop

test: .develop
	@py.test -q ./tests

vtest: .develop
	@py.test -s -v ./tests

cov cover coverage:
	tox

cov-dev: .develop
	@echo "Run without extensions"
	@py.test --cov=aioactor tests
	@py.test --cov=aioactor --cov-report=term --cov-report=html --cov-append tests
	@echo "open file://`pwd`/htmlcov/index.html"

clean:
	@rm -rf `find . -name __pycache__`
	@rm -f `find . -type f -name '*.py[co]' `
	@rm -f `find . -type f -name '*~' `
	@rm -f `find . -type f -name '.*~' `
	@rm -f `find . -type f -name '@*' `
	@rm -f `find . -type f -name '#*#' `
	@rm -f `find . -type f -name '*.orig' `
	@rm -f `find . -type f -name '*.rej' `
	@rm -f .coverage
	@rm -rf htmlcov
	@rm -rf build
	@rm -rf cover
	@make -C docs clean
	@python setup.py clean
	@rm -rf .tox
	@rm -f .develop
	@rm -f .flake
	@rm -f .install-deps
	@rm -rf aioactor.egg-info

doc:
	@make -C docs html SPHINXOPTS="-W -E"
	@echo "open file://`pwd`/docs/_build/html/index.html"

doc-spelling:
	@make -C docs spelling SPHINXOPTS="-W -E"

install:
	@pip install -U pip
	@pip install -Ur requirements/dev.txt

.PHONY: all build flake test vtest cov clean doc