test:
	pytest tests/test_back.py
	pytest tests/test_masks.py
	pytest tests/test_tools.py
	pytest tests/test_basic_beam_size.py
	pytest tests/test_no_noise.py
	pytest tests/test_noise.py
	pytest tests/test_iso_noise.py
	pytest tests/test_gaussian.py

html:
	cd docs && python -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build
	open docs/_build/index.html

lint:
	-pylint laserbeamsize/__init__.py
	-pylint laserbeamsize/analysis.py
	-pylint laserbeamsize/background.py
	-pylint laserbeamsize/display.py
	-pylint laserbeamsize/gaussian.py
	-pylint laserbeamsize/masks.py
	-pylint laserbeamsize/image_tools.py
	-pylint laserbeamsize/m2_fit.py
	-pylint laserbeamsize/m2_display.py
	-pylint tests/test_all_notebooks.py


doccheck:
	-pydocstyle laserbeamsize/__init__.py
	-pydocstyle laserbeamsize/analysis.py
	-pydocstyle laserbeamsize/background.py
	-pydocstyle laserbeamsize/display.py
	-pydocstyle laserbeamsize/gaussian.py
	-pydocstyle laserbeamsize/image_tools.py
	-pydocstyle laserbeamsize/masks.py
	-pydocstyle laserbeamsize/m2_fit.py
	-pydocstyle laserbeamsize/m2_display.py

rstcheck:
	-rstcheck README.rst
	-rstcheck CHANGELOG.rst
	-rstcheck docs/index.rst
	-rstcheck docs/changelog.rst
	-rstcheck --ignore-directives automodapi docs/analysis.rst
	-rstcheck --ignore-directives automodapi docs/background.rst
	-rstcheck --ignore-directives automodapi docs/display.rst
	-rstcheck --ignore-directives automodapi docs/image_tools.rst
	-rstcheck --ignore-directives automodapi docs/m2_display.rst
	-rstcheck --ignore-directives automodapi docs/m2_fit.rst
	-rstcheck --ignore-directives automodapi docs/masks.rst

rcheck:
	make clean
	make test
	make lint
	make doccheck
	make rstcheck
	touch docs/*ipynb
	touch docs/*rst
	make html
	check-manifest
	pyroma -d .
	pytest --verbose tests/test_all_notebooks.py


clean:
	rm -rf .eggs
	rm -rf .pytest_cache
	rm -rf .virtual_documents
	rm -rf __pycache__
	rm -rf dist
	rm -rf laserbeamsize.egg-info
	rm -rf laserbeamsize/__pycache__
	rm -rf docs/_build
	rm -rf docs/api
	rm -rf docs/.ipynb_checkpoints
	rm -rf tests/__pycache__
	rm -rf build


.PHONY: clean rcheck html notecheck pycheck doccheck test rstcheck