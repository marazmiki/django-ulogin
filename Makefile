test:
	python setup.py test

flake8:
	flake8 --ignore=E501 --max-complexity 12 django_ulogin

coverage:
	coverage run --include=django_ulogin/* setup.py test
	coverage html

