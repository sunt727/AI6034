from __future__ import print_function
import torch
import time

# Construct a 5x3 matrix, uninitialized:
x = torch.Tensor(5, 3)
print(x)

# Get its size
print(x.size())


# Addition: syntax 1
y = torch.rand(5, 3)
print(x + y)

# Addition: syntax 2
print(torch.add(x, y))

# Addition: giving an output tensor

result = torch.Tensor(5, 3)
torch.add(x, y, out=result)
print(result)

# Addition: in-place
# adds x to y
y.add_(x)
print(y)

# You can use standard numpy-like indexing with all bells and whistles!
print(x[:, 1])

# Converting torch Tensor to numpy Array
a = torch.ones(5)
print(a)
b = a.numpy()
print(b)

# See how the numpy array changed in value.
a.add_(1)
print(a)
print(b)

#See how changing the np array changed the torch Tensor automatically
import numpy as np
a = np.ones(5)
b = torch.from_numpy(a)
np.add(a, 1, out=a)
print(a)
print(b)

start = time.time()
print("CUDA ISNT RUNNING!!!", x + y)
elapsed = time.time()
print("It costs %6f sec" % (elapsed - start))

# Tensors can be moved onto GPU using the .cuda function.
# let us run this cell only if CUDA is available
if torch.cuda.is_available():
    start = time.time()
    x = x.cuda()
    y = y.cuda()
    print("CUDA IS RUNNING!!!", x + y)
    elapsed = time.time()
    print("It costs %6f sec" % (elapsed - start))



