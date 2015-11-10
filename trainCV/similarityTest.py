#similarity.py
from scipy.spatial import distance as dist
import numpy as np


np.random.seed(42)

x = np.random.rand(4)
y = np.random.rand(4)

print x
print y

#Euclidean distance
print "Euclidean Distance {0}".format(dist.euclidean(x,y))

#City-Block distance
print "City-block Distance {0}".format(dist.cityblock(x,y))

#Chebyshev distance
print "Chebyshev Distance {0}".format(dist.chebyshev(x,y))



