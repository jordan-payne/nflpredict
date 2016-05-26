init:
	pip install -r requirements.txt
clean:
	-rm -f -v */*.pyc
	-rm ghostdriver.log
	-rm .DS_Store
	-rm -rf **/__pycache__
test: pytest clean
pytest:
	py.test
