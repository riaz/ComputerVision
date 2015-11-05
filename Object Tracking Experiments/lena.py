import pylab
import matplotlib.colors
import numpy

im = pylab.imread('lena_gray.png').sum(axis=2) # make grayscale
pylab.imshow(im, cmap=pylab.cm.gray)
pylab.title('orig')
imvals = numpy.sort(im.flatten())
lo = imvals[0]
hi = imvals[-1]
steps = (imvals[::len(imvals)/256] - lo) / (hi - lo)
num_steps = float(len(steps))
interps = [(s, idx/num_steps, idx/num_steps) for idx, s in enumerate(steps)]
interps.append((1, 1, 1))
cdict = {'red' : interps,
         'green' : interps,
         'blue' : interps}
histeq_cmap = matplotlib.colors.LinearSegmentedColormap('HistEq', cdict)
pylab.figure()
pylab.imshow(im, cmap=histeq_cmap)
pylab.title('histeq')
pylab.show()
