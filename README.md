# Example Package
pip install --upgrade setuptools
pip install --upgrade wheel
python -m pip install build
python -m build
pip install twine
twine upload dist/*
twine upload --skip-existing dist/*

# cli
pip install -e .
[project.scripts]
hello-world = "fiver:hello_world"

[project]
# ...
dependencies = [
    "docutils",
    "BazSpam == 1.1",
]