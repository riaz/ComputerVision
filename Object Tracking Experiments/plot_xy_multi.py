from matplotlib import pyplot as plt
import numpy as np

t = np.arange(0,5,0.2)

plt.plot(t,t,'r--',t,t**2, 'bs',t,t**3,'g^') #multi legend
#The edge points cutt-off ,so we extend the axes 0 - 6 in x, 0-20 y

plt.show()
