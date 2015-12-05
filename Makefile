.PHONY: test clean publish docker

test:
	MONGO=$(value MONGO) tox

clean:
	rm .coverage
	rm -rf build dist mongoext.egg-info

publish: test
	python setup.py sdist bdist_wheel upload
