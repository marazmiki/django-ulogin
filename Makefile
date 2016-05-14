project_name=django_ulogin


test:
	python setup.py test


release:
	python setup.py sdist --format=zip,bztar,gztar register upload
	python setup.py bdist_wheel register upload


flake8:
	flake8 ${project_name} setup.py tests.py


coverage:
	make clean
	python setup.py develop
	coverage run --rcfile=.coveragerc --include=${project_name}/* setup.py test
	coverage report
	coverage html
	python setup.py develop --uninstall


clean:
	python setup.py develop --uninstall
	rm -rf *.egg-info *.egg
	rm -rf htmlcov
	rm -f .coverage
	find . -name "*.pyc" -exec rm -rf {} \;


coveralls:
	coveralls


