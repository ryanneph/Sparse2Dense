import pyximport; pyximport.install()
import sys
from . import sparserecon
import numpy as np
from scipy.io import loadmat

def reconstruct_sparse(idx, val, shape, decrement=False, transpose=False):
    """just make sure datatypes match expectation in cython function"""
    idx = np.asarray(idx, dtype='int64').reshape(-1)
    val = np.asarray(val, dtype='float64').reshape(-1)
    return sparserecon.reconstruct(idx, val, shape, decrement, transpose).reshape(shape)

def reconstruct_from_dosecalc_mat(fname, beamletnum=None):
    """parse output of dosecalc_legacy and return output based on value of beamletnum:
        switch (beamletnum)
            case None: a summed array of all beamlet dose, or a list of individual beamlet dose arrays
            case list[int]: list of individual beamlet dose arrays for beamlet index matching values in list
            case int: single beamlet array whose index matches provided int
    """
    mat = loadmat(fname)
    shape = mat['ct'].ravel().tolist()
    shape = [shape[2], shape[0], shape[1]] # ZYX order
    pairs = []
    for k in mat.keys():
        if k[0] == 'I':
            pairs.append( (k, k.replace('I','n')) )

    if isinstance(beamletnum, int):
        kidx, kval = pairs[beamletnum]
        return reconstruct_sparse( mat[kidx], mat[kval], shape, decrement=True, transpose=False )

    if isinstance(beamletnum, list):
        outputs = []
        for bn in beamletnum:
            kidx, kval = pairs[bn]
            outputs.append(reconstruct_sparse( mat[kidx], mat[kval], shape, decrement=True, transpose=False ))
        return outputs

    else:
        # sum beamlets together
        outarr = np.zeros(shape, dtype=np.float64)
        for kidx, kval in pairs:
            outarr += reconstruct_sparse( mat[kidx], mat[kval], shape, decrement=True, transpose=False )
        return outarr


if __name__ == '__main__':
    spdata = "/media/hdd1/projects/dosecalc_legacy/D_data/lung/lung_gantry_-90_couch_90_beamlet.mat"
    numdata = "/media/hdd1/projects/dosecalc_legacy/D_data/lung/lung_gantry_-90_couch_90_beamletnum.mat"
    dosedata = "/media/hdd1/projects/dosecalc_legacy/D_data/lung/dosefile/lung_gantry_-90_couch_90_gpupencil.mat"
    dense = reconstruct_from_dosecalc_mat(dosedata)
    #  dense = np.transpose(dense, [2,1,0])
    from pymedimage.rttypes import BaseVolume
    d = BaseVolume.fromArray(dense.astype(np.float32)).toHDF5(dosedata)

    #  """example"""
    #  idx = [35000, 2, 6, 7]
    #  val = [10, 2, 3, 4]
    #  shape = (200, 200)
    #  dense = reconstruct_sparse(idx, val, shape).reshape(shape)
    #  import matplotlib.pyplot as plt
    #  plt.imshow(dense)
    #  plt.show()
