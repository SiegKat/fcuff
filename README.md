[![Documentation Status](https://readthedocs.org/projects/fcuff)](https://fcuff.readthedocs.io/en/latest/?badge=latest) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# fcuff
`fcuff` is a Python package which streamlines electrochemical data analysis. 

`fcuff` includes both a standard Python package which can be used programmatically and incorporated into an existing workflow, as well as a standalone graphical user interface for interactive use.

If you have a feature request or find a bug, please file an [issue](https://github.com/SiegKat/fcuff/issues) or submit a [pull request](https://github.com/SiegKat/fcuff/pulls). This is designed to be an open-source tool which the entire electrochemical community can build upon and use.

## Installation
`fcuff` can be installed from PyPI using `pip`:

```bash
pip install fcuff
```

## Documentation
The documentation can be found at [fcuff.readthedocs.io](https://fcuff.readthedocs.io/en/latest/) 

##  Package Structure
- `datums.py`: Data processing functions
- `visuals.py`: Data visualization functions
- `utils.py`: File handling and general auxilliary functions
- `model.py`:  `Datum` class to store electrochemical data along with associated features  and expereimental parameters

## License
[MIT](https://choosealicense.com/licenses/mit/) 
