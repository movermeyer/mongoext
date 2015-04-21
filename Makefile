.PHONY: test mongo clean publish

test:
	flake8
	nosetests --with-coverage --cover-package=mongoext

mongo:
	docker run --name mongoext -p 27017:27017 -d mongo

clean:
	rm -rf build dist mongoext.egg-info

publish: test
	python setup.py sdist bdist_wheel upload
