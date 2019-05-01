project_name=django_ulogin

.PHONY: test
test:
	python setup.py test

.PHONY: release
release:
	./setup.py sdist bdist_wheel
	twine check dist/*
	twine upload dist/*

.PHONY: clean
clean:
	python setup.py develop --uninstall
	rm -rf *.egg-info *.egg
	rm -f .coverage
	find ${project_name} -name "*.pyc" -exec rm -rf {} \;



