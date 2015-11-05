from matplotlib import pyplot as plt

plt.plot([1,2,3,4],[1,4,9,16],'bx') #blue cross
#The edge points cutt-off ,so we extend the axes 0 - 6 in x, 0-20 y
plt.axis([0,6,0,20])
plt.show()
