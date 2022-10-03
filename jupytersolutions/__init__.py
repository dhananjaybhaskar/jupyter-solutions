
import json
import os
from copy import deepcopy


import sys

def process_cell(cell, keep_keyword, strip_keyword):
    """
    Removes lines which end with the trigger '#{keyword}'
    """
    cell = deepcopy(cell)
    source = []
    if len(cell['source']) == 0:
        return cell
    if cell['source'][0].startswith(f"#{strip_keyword}"):
        return None
    for line in cell['source']:
        if line.strip().endswith(f"#{strip_keyword}"):
            continue
        newline = line.replace(f"#{keep_keyword}", "")
        if line.isspace() or not newline.isspace():
            source.append(newline)
    cell['source'] = source
    return cell

def process_doc(main,
                original_doc,
                append_string,
                keep_keyword,
                strip_keyword,
                fix_numbers = True):
    try:
        original_doc['metadata']['jupytext']['formats'] = "ipynb"
    except:
        pass
    cells = [process_cell(cell, keep_keyword, strip_keyword) for cell in original_doc['cells']]
    cells = [cell for cell in cells if cell is not None]
    doc = deepcopy(original_doc)
    doc['cells'] = cells
    if fix_numbers:
        doc = fix_numbers_doc(doc)
    newfilename = main.replace("-main",append_string)
    with open(newfilename,"w") as f:
        print("Writing " + newfilename)
        json.dump(doc,f)
    os.system("jupyter trust " + newfilename)

def write_all(filename=None):
    if filename is None:
        for name in os.listdir("."):
            if "-main.ipynb" in name:
                print("Using " + name)
                filename = name
                break
    if filename is None:
        raise Exception("No main file given or found")
    with open(filename) as f:
        doc = json.load(f)

    process_doc(filename, doc, "-sol", "solution", "worksheet") # solutions
    process_doc(filename, doc, "", "worksheet", "solution") # worksheet

def fix_numbers_doc(doc):
    i = 0
    for cell in doc['cells']:
        if 'execution_count' in cell and cell['execution_count'] is not None:
            i += 1
            cell['execution_count'] = i
            for output in cell['outputs']:
                if 'execution_count' in output and output['execution_count'] is not None:
                    output['execution_count'] = i
    return doc

def fix_numbers(filename):
    import json
    with open(filename) as f:
        doc = json.load(f)
    with open(filename, "w") as f:
        json.dump(fix_numbers_doc(doc), f)
    os.system("jupyter trust " + filename)
