test:
	flake8
	nosetests --with-coverage --cover-package=mongoext

mongo:
	docker run --name mongoext -p 27017:27017 -d mongo
