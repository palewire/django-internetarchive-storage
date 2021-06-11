.PHONY: test ship

test:
	pipenv run flake8 ./ia_storage
	pipenv run coverage run example/manage.py test ia_storage
	pipenv run coverage report -m


ship:
	rm -rf build/
	rm -rf dist/
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/* --skip-existing
