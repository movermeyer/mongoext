.PHONY: test clean publish docker

test:
	flake8
	nosetests --with-coverage --cover-package=mongoext

clean:
	rm .coverage
	rm -rf build dist mongoext.egg-info

publish: test
	python setup.py sdist bdist_wheel upload

docker:
	@echo "Run: export DOCKER_HOST=\"tcp://`vagrant ssh-config | sed -n "s/[ ]*HostName[ ]*//gp"`:2375\""
