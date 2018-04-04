import numpy as np
from chainer import cuda


def mask_to_bbox(mask):
    """Compute the bounding boxes around the masked region.

    This function accepts both :obj:`numpy.ndarray` and :obj:`cupy.ndarray` as
    inputs.

    Args:
        mask (array): An array whose shape is :math:`(N, H, W)`.
            :math:`N` is the number of masks.
            The dtype should be :obj:`numpy.bool`.

    Returns:
        array:
        An array whose shape is :math:`(N, 4)`.
        :math:`N` is the number of bounding boxes.
        The dtype should be :obj:`numpy.float32`.

    """
    _, H, W = mask.shape
    xp = cuda.get_array_module(mask)

    # CuPy does not support argwhere yet
    mask = cuda.to_cpu(mask)

    bbox = []
    for msk in mask:
        where = np.argwhere(msk)
        y_min, x_min = where.min(0)
        y_max, x_max = where.max(0) + 1
        bbox.append((y_min, x_min, y_max, x_max))
    return xp.array(bbox)
