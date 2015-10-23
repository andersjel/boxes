PYTHONPATH := ${PWD}/src:${PYTHONPATH}
export PYTHONPATH

py-files = $(shell find src/ -name '*.py')
examples = $(patsubst %.py, %.svg, $(wildcard examples/*.py))
doc-files = $(shell find doc/ -name '*.rst') doc/conf.py

.PHONY: doc
doc: doc/_build/stamp

doc/_build/stamp: ${examples} ${py-files} ${doc-files}
	cd doc && make html
	touch $@

.PHONY: doctest
doctest:
	cd doc && make doctest

.PHONY: unittest
unittest:
	py.test tests

.PHONY: test
test:
	py.test --doctest-modules src tests

.PHONY: examples
examples: ${examples}

examples/%.svg: examples/%.py ${py-files}
	python $< $@

.PHONY: pretty
pretty:
	autopep8 --indent-size 2 -ir src/

.PHONY: clean
clean:
	rm -f examples/*.svg
	rm -rf doc/_build
