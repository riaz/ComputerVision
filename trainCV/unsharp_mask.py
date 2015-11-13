#Program to demonstrate unsharp masking

from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import filters


im = np.array(Image.open("lena_noisy.png").convert("L"))
blur = filters.gaussian_filter(im,10)
sharp = im - blur

plt.figure("Unsharp masking Example")
plt.gray()

plt.subplot(131)
plt.title("Original")
plt.imshow(im)

plt.subplot(132)
plt.title("Gaussian Blur Image")
plt.imshow(blur)

plt.subplot(133)
plt.title("Blur Subtracted Image")
plt.imshow(sharp)

plt.show()


