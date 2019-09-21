
import json
import os
from copy import deepcopy

def write_worksheet(filename=None):
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

    sol_cells = []
    worksheet_cells = []

    for cell in doc['cells']:
        if 'outputs' in cell:
            cell['outputs'] = []
        if 'execution_count' in cell:
            cell['execution_count'] = None
        worksheet_source = []
        sol_source = []
        for line in cell['source']:
            if line.startswith("# solution"):
                break
            if not line.strip().endswith(" # solution"):
                worksheet_source.append(line.replace(" # worksheet",""))
        for line in cell['source']:
            if line.startswith("# worksheet"):
                break
            if not line.strip().endswith(" # worksheet"):
                sol_source.append(line.replace(" # solution",""))
        cell['source'] = worksheet_source
        worksheet_cells.append(deepcopy(cell))
        cell['source'] = sol_source
        sol_cells.append(deepcopy(cell))
        
    doc['cells'] = sol_cells
    with open(filename.replace("-master","-sol"),"w") as f:
        print("Writing " + filename.replace("-master","-sol"))
        json.dump(doc, f)

    doc['cells'] = worksheet_cells
    with open(filename.replace("-master",""), "w") as f:
        print("Writing " + filename.replace("-master",""))
        json.dump(doc, f)