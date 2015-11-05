py-files = $(shell find src/ -name '*.py')
examples = $(patsubst %.py, %.svg, $(wildcard examples/*.py))
doc-files = $(shell find doc/ -name '*.rst') doc/conf.py
export PATH := $(PWD)/venv/bin:$(PATH)

.PHONY: doc
doc: doc/_build/stamp

doc/_build/stamp: ${examples} ${py-files} ${doc-files} venv/stamp
	cd doc && make html
	touch $@

.PHONY: doctest
doctest: venv/stamp
	cd doc && make doctest

.PHONY: unittest
unittest: venv/stamp
	python -m pytest tests

.PHONY: test
test: doctest unittest

.PHONY: examples
examples: ${examples}

examples/%.svg: examples/%.py ${py-files} venv/stamp
	python $< $@

.PHONY: pretty
pretty:
	autopep8 --indent-size 2 -ir src/ tests/

.PHONY: clean
clean:
	rm -f examples/*.svg
	rm -rf doc/_build
	rm -rf venv

venv/stamp:
	pyvenv --clear --system-site-packages venv
	python -m pip install -e .
	touch $@
