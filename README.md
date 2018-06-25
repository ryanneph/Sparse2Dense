# Sparse2Dense
This snippet was written to efficiently convert a sparse rank-3 tensor in [COO format](https://en.wikipedia.org/wiki/Sparse_matrix#Coordinate_list_(COO)) (key-value mapping between linearized index and corresponding value for every non-zero valued element in the tensor) to a dense volume of the appropriate shape.

A general conversion function is exposed as well as a wrapper that handles a specific format used in my research lab for storing sparse x-ray beamlet dose for radiation treatment planning purposes (COO embedded in a .mat file with Fortran data ordering).

## Installing
`cd` to the root directory of the locally cloned repository, then run: `pip install .`

Alternatively, from the same directory, run `python setup.py install`
