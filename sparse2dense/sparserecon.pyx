import cython
cimport numpy as np
import numpy as np

@cython.boundscheck(False)
@cython.wraparound(False)
def reconstruct(np.ndarray[np.int64_t, ndim=1] idx, np.ndarray[np.float64_t, ndim=1] val, shape, decrement=False, transpose=False):
    """reconstruct a dense array with 'size' from the two column sparse array in COO format with
    indices 'idx' and corresponding non-zero values 'vals'

    Args:
        idx: vector of 64bit integer indices (linear) in ZYX ordering (row-major; C)
        val: vector of 64bit double values corresponding to positions in 'idx'
        shape (tuple): size of dense tensor in same order as data (ZYX)
        decrement: if data came from 1-indexed language (matlab), subtract 1 from index
        transpose: flip X-Y axes?
    """
    cdef int ii
    cdef int _i, y, x, z
    cdef np.ndarray[np.float64_t, ndim=1] outarr = np.zeros(np.prod(shape), dtype=np.float64)
    assert(idx.size == val.size)
    for ii in range(idx.size):
        _i = idx[ii] - int(decrement);
        if (transpose):
            y = _i % shape[1]
            x = (_i/shape[1])%shape[2]
            z = _i/(shape[1]*shape[2])
            _i = x + shape[2]*(y + shape[1]*z)
        outarr[ _i ] = val[ii]
    return outarr
