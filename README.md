
# jupyter-solutions


1. Install this Python package:

    ```python
    pip install git+https://github.com/sswatson/jupyter-solutions
    ```

2. Make a Jupyter notebook. End lines or begin cells with ` # solution` and ` # worksheet` to make them visible only in the worksheet or solutions version. Choose a file name that ends in `-master.ipynb`. 

3. Type `python` at the command line and run the following two lines of code:

    ```python
    from jupytersolutions import write_worksheet
    write_worksheet()
    ```
