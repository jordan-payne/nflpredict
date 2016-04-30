init:
	pip install -r requirements.txt
clean:
	rm -f -v */*.pyc
test:
	py.test
