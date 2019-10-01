
import json
import os
from copy import deepcopy

def clean_cell(cell):
    if 'execution_count' in cell:
        cell['execution_count'] = None

def process_cell(cell, keep_keyword, strip_keyword):
    """
    Cleans the cell and removes lines which 
    end with the trigger '# {keyword}'
    """
    cell = deepcopy(cell)
    clean_cell(cell)
    source = []
    if len(cell['source']) == 0:
        return cell
    if cell['source'][0].startswith(f"# {strip_keyword}"):
        return None
    for line in cell['source']:
        if line.strip().endswith(f"# {strip_keyword}"):
            continue
        newline = line.replace(f"# {keep_keyword}","")
        if line.isspace() or not newline.isspace():
            source.append(newline)
    cell['source'] = source
    return cell

def process_doc(master, 
                original_doc, 
                append_string, 
                keep_keyword, 
                strip_keyword):
    cells = [process_cell(cell, keep_keyword, strip_keyword) for cell in original_doc['cells']]
    cells = [cell for cell in cells if cell is not None]
    doc = deepcopy(original_doc)
    doc['cells'] = cells
    with open(master.replace("-master",append_string),"w") as f:
        print("Writing " + master.replace("-master",append_string))
        json.dump(doc,f)

def write_all(filename=None):
    if filename is None:
        for name in os.listdir("."):
            if "-master.ipynb" in name:
                print("Using " + name)
                filename = name
                break
    if filename is None:
        raise Exception("No master file given or found")
    with open(filename) as f:
        doc = json.load(f)
        
    process_doc(filename, doc, "-sol", "solution", "worksheet") # solutions
    process_doc(filename, doc, "", "worksheet", "solution") # worksheet
