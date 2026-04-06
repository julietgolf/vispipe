import numpy as np

def read_unstruct_grd(path):
    with np.load(path) as unstruct:
        nodes=unstruct["nodes"]
        elemcomps=unstruct["elemcomps"]
        depth=unstruct["depth"]

    return nodes,elemcomps,depth

def read_data(path,key="data"):
    with np.load(path) as d:
        data=d[key]
    
    return data