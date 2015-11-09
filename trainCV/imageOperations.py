#Create a thumbnail and other image opertions using PIL library
from PIL import Image
from matplotlib import pyplot as plt


pil_im = Image.open('riaz.jpg')
print "Image Original Size : {0} ".format(pil_im.size)
plt.subplot(141)
plt.imshow(pil_im)

pil_im.thumbnail((480,640))
print "Image Thumbnail Size : {0} ".format(pil_im.size)
plt.subplot(142)
plt.imshow(pil_im)

#cropping
box = (50,50,200,400)
region = pil_im.crop(box)
region = region.transpose(Image.ROTATE_180)

pil_im.paste(region,box)

plt.subplot(143)
plt.imshow(pil_im)

pil_im = pil_im.rotate(45)
plt.subplot(144)
plt.imshow(pil_im)


plt.xticks([]),plt.yticks([])
plt.show()

