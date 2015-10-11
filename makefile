PYTHONPATH := ${PWD}/src:${PYTHONPATH}
export PYTHONPATH

py-files = $(shell find src/ -name '*.py')
examples = $(patsubst %.py, %.svg, $(wildcard examples/*.py))
doc-files = $(wildcard doc/*.rst) doc/conf.py

.PHONY: doc
doc: doc/_build/stamp

doc/_build/stamp: ${examples} ${py-files} ${doc-files}
	cd doc && make html
	touch $@

.PHONY: doctest
doctest:
	cd doc && make doctest

.PHONY: examples
examples: ${examples}

examples/%.svg: examples/%.py ${py-files}
	python $< $@

clean:
	rm -f examples/*.svg
	rm -rf doc/_build
