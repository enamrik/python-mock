
install_deps:
	test -d .venv || virtualenv .venv
	. .venv/bin/activate; pip install -e .;

test_only:
	. .venv/bin/activate; pip install -r dev-requirements.txt; pytest -v -s;

test: install_deps test_only
