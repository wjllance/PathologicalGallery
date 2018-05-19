import openslide
from skimage import io
import numpy as np
import sys

fname=sys.argv[1]
osh=openslide.OpenSlide(fname)
thumb=np.array(osh.get_thumbnail((500,500)))
io.imsave(sys.argv[2],thumb)

