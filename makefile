PYTHONPATH := ${PWD}/src:${PYTHONPATH}
export PYTHONPATH

examples = $(patsubst %.py, %.svg, $(wildcard examples/*.py))

.PHONY: doc
doc: ${examples}
	cd doc && make html

.PHONY: examples
examples: ${examples}

examples/%.svg: examples/%.py $(shell find src/ -name '*.py')
	python $< $@

clean:
	rm -f examples/*.svg
	rm -rf doc/_build
