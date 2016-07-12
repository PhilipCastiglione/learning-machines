import numpy

print("Hello World!")

a = numpy.array([1,2,3])
print(a)
print(a * 2)

print("wtf maths with arrays")

# what is this?
b = numpy.array([1, True, 'derp'])
print(b)

# and this?

c = numpy.array([1, True])
print(c)

import matplotlib.pyplot as plt

derp = [1,1,2,2,3,4,5,5,6,7,7,8,8,9,10]

plt.hist(derp)
plt.show()
