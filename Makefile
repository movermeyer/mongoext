.PHONY: test clean publish docker

test:
	MONGO=$(value MONGO) tox

publish: test
	python setup.py sdist bdist_wheel upload
