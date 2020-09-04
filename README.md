
# jupyter-solutions


1. Install this Python package:

    ```python
    pip install git+https://github.com/sswatson/jupyter-solutions
    ```

2. Make a Jupyter notebook. End lines or begin cells with `#solution` and `#worksheet` to make them visible only in the solutions or worksheet version. You can also end a single line in a cell with `#solution` or `#worksheet` to ensure that it only shows up in one of the two versions. Choose a file name that ends in `-master.ipynb`.

3. Type `python` at the command line and run the following two lines of code:

    ```python
    from jupytersolutions import write_all
    write_all()
    ```
