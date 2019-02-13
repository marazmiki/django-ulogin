project_name=django_ulogin


test:
	python setup.py test


release:
	./setup.py sdist bdist_wheel
	twine check dist/*
	twine upload dist/*

flake8:
	flake8 .


coverage:
	python setup.py develop
	coverage run --include=${project_name}/* setup.py test
	coverage report
	rm -rf htmlcov
	coverage html
	python setup.py develop --uninstall


clean:
	python setup.py develop --uninstall
	rm -rf *.egg-info *.egg
	rm -f .coverage
	find ${project_name} -name "*.pyc" -exec rm -rf {} \;



