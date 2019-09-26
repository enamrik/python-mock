# Python-Mock

## Installation

Put python-mock in the `extras_require` section of your setup.py. 

```python
    ...
    extras_require={
        'dev': [
            'python-mock@git+ssh://git@github.com/enamrik/python-mock.git'
        ]
    }
    ...
```

Install extras by running:

```bash
pip install -e ".[dev]"
```

