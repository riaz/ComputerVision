from PIL import Image
from matplotlib import pyplot as plt
import os



pil_im = Image.open('riaz.jpg').convert('L')

plt.imshow(pil_im)
plt.xticks([]),plt.yticks([])
plt.show()
