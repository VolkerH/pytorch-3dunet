import pathlib
import skimage.io
import matplotlib.pyplot as plt
import numpy as np

basepath = "/g/ml2018/cryo18/dlcourse"

toplevel = pathlib.Path(basepath) 
files = toplevel.rglob("drp*.tif")
deconvolved = list( filter(lambda x: "deconv.tif" in str(x), files))
files = toplevel.rglob("drp*.tif")

raw = list(filter(lambda x: "deconv.tif" not in str(x), files))
rawbase = list(map(lambda x: str(x.name), raw))
rawstem = list(map(lambda x: str(x.stem), raw))

# match files
def _return_matching_deconvolved(raw):
    stem = raw.stem
    match = filter(lambda x: stem in str(x), deconvolved)
    return list(match)[0]


def read_pair(pair):
    return list(map(lambda x: skimage.io.imread(str(x)), pair))

def create_h5_from_pair(pair):
    raw, decon = read_pair(pair)
    raw=raw.astype(decon.dtype)
    raw -= 100 # fix camera offset
    np.clip(raw, a_min=0, a_max=None)
    outfile = "/g/ml2018/cryo18/h5/" + pair[0].stem + ".h5"
    print("      - '" +outfile + "'")
    with h5py.File(outfile, "w") as f:
        f["raw"]=raw
        f["deconvolved"]=decon
    return("done")


pairs = list(map(lambda x: (x, _return_matching_deconvolved(x)), raw))
list(map(create_h5_from_pair, pairs[::10]))