export PATH := $(PWD)/venv/bin:$(PATH)

py-files = $(shell find src/ -name '*.py')
doc-files = \
	doc/conf.py \
	$(shell find doc/ -name '*.rst') \
	$(shell find doc/figures/ )

.PHONY: doc
doc: doc/_build/stamp

doc/_build/stamp: ${py-files} ${doc-files} venv/stamp
	cd doc && make html
	touch $@

doc/figures:
	mkdir $@

.PHONY: doctest
doctest: venv/stamp | doc/figures
	cd doc && make doctest

.PHONY: unittest
unittest: venv/stamp
	python -m pytest tests

.PHONY: test
test: doctest unittest

.PHONY: pretty
pretty:
	autopep8 --indent-size 2 -ir src/ tests/

.PHONY: clean
clean:
	rm -f examples/*.svg
	rm -rf doc/_build
	rm -rf venv
	rm -rf doc/figures

venv/stamp:
	pyvenv --clear --system-site-packages venv
	python -m pip install -e .
	touch $@
