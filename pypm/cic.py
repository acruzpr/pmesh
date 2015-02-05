# cloud in cell painting
#
import numpy

def paint(pos, mesh, weights=1.0, mode="raise", period=None, transform=None):
    """ CIC approximation (trilinear), painting points to Nmesh,
        each point has a weight given by weights.
        This does not give density.
        pos is supposed to be row vectors. aka for 3d input
        pos.shape is (?, 3).

        pos[:, i] should have been normalized in the range of [ 0,  mesh.shape[i] )

        thus z is the fast moving index

        mode can be :
            "raise" : raise exceptions if a particle is painted
             outside the mesh
            "ignore": ignore particle contribution outside of the mesh
        period can be a scalar or of length len(mesh.shape). if period is given
        the particles are wrapped by the period.

        transform is a function that transforms pos to mesh units:
        transform(pos[:, 3]) -> meshpos[:, 3]
    """
    pos = numpy.array(pos)
    chunksize = 1024 * 16 * 4
    Ndim = pos.shape[-1]
    Np = pos.shape[0]

    if transform is None:
        transform = lambda x:x
    neighbours = ((numpy.arange(2 ** Ndim)[:, None] >> \
            numpy.arange(Ndim)[None, :]) & 1)
    for start in range(0, Np, chunksize):
        chunk = slice(start, start+chunksize)
        if numpy.isscalar(weights):
          wchunk = weights
        else:
          wchunk = weights[chunk]
        if mode == 'raise':
            gridpos = transform(pos[chunk])
            rmi_mode = 'raise'
            intpos = numpy.intp(numpy.floor(gridpos))
        elif mode == 'ignore':
            gridpos = transform(pos[chunk])
            rmi_mode = 'raise'
            intpos = numpy.intp(numpy.floor(gridpos))

        for i, neighbour in enumerate(neighbours):
            neighbour = neighbour[None, :]
            targetpos = intpos + neighbour

            kernel = (1.0 - numpy.abs(gridpos - targetpos)).prod(axis=-1)
            add = wchunk * kernel

            if period is not None:
                numpy.remainder(targetpos, period, targetpos)

            if mode == 'ignore':
                # filter out those outside of the mesh
                mask = (targetpos >= 0).all(axis=-1)
                for d in range(Ndim):
                    mask &= (targetpos[..., d] < mesh.shape[d])
                targetpos = targetpos[mask]
                add = add[mask]

            if len(targetpos) > 0:
                targetindex = numpy.ravel_multi_index(
                        targetpos.T, mesh.shape, mode=rmi_mode)
                u, label = numpy.unique(targetindex, return_inverse=True)
                mesh.flat[u] += numpy.bincount(label, add, minlength=len(u))

    return mesh

from tools import Timers
RT = Timers()
def readout(mesh, pos, mode="raise", period=None, transform=None):
    """ CIC approximation, reading out mesh values at pos,
        see document of paint. 
    """
    pos = numpy.array(pos)
    value = numpy.zeros(len(pos), dtype='f8')
    chunksize = 1024 * 16 * 4
    Ndim = pos.shape[-1]
    Np = pos.shape[0]
    if transform is None:
        transform = lambda x: x

    neighbours = ((numpy.arange(2 ** Ndim)[:, None] >> \
            numpy.arange(Ndim)[None, :]) & 1)
    for start in range(0, Np, chunksize):
        chunk = slice(start, start+chunksize)
        with RT['transform']:
            if mode == 'raise':
                gridpos = transform(pos[chunk])
                rmi_mode = 'raise'
                intpos = numpy.intp(numpy.floor(gridpos))
            elif mode == 'ignore':
                gridpos = transform(pos[chunk])
                rmi_mode = 'raise'
                intpos = numpy.intp(numpy.floor(gridpos))

        with RT['iteration']:
            for i, neighbour in enumerate(neighbours):
                neighbour = neighbour[None, :]
                with RT['shift']:
                    targetpos = intpos + neighbour

                    kernel = (1.0 - numpy.abs(gridpos - targetpos)).prod(axis=-1)

                    if period is not None:
                        numpy.remainder(targetpos, period, targetpos)

                with RT['masking']:
                    if mode == 'ignore':
                        # filter out those outside of the mesh
                        mask = (targetpos >= 0).all(axis=-1)
                        for d in range(Ndim):
                            mask &= (targetpos[..., d] < mesh.shape[d])
                        targetpos = targetpos[mask]
                        kernel = kernel[mask]
                    else:
                        mask = Ellipsis

                with RT['ravel']:
                    if len(targetpos) > 0:
                        targetindex = numpy.ravel_multi_index(
                                targetpos.T, mesh.shape, mode=rmi_mode)
                        value[chunk][mask] += kernel * mesh.flat[targetindex]
    return value


