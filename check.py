import itertools
import numpy as np
from experiments import clique_indices,count,present
for n in range(3,8):
    for k in range(3,min(n,5)+1):
        ix=clique_indices(n,k)
        for bits in itertools.islice(itertools.product((0,1),repeat=n*(n-1)//2),32):
            x=np.asarray(bits,dtype=np.uint8)
            assert (count(x,ix)>0)==present(x,n,k)
ix=clique_indices(5,3)
zeros=sum(count(np.asarray(bits,dtype=np.uint8),ix)==0 for bits in itertools.product((0,1),repeat=10))
assert zeros==12,zeros
print('Independent detectors agree; 12/1024 K5 colorings avoid monochromatic K3.')
