"""Rerun the independent fixed-grid simulation reported in Sections 3–4.

With seed 20260928 and the same NumPy bit generator, results.json matches the
paper's baseline. Older trials from the user's first draft remain unavailable.
"""
import argparse,json,math,platform
from pathlib import Path
import numpy as np
from experiments import clique_indices,count

def sample(n,k,trials,seed):
    rng=np.random.default_rng(seed);ix=clique_indices(n,k)
    return np.array([count(rng.integers(0,2,size=math.comb(n,2),dtype=np.uint8),ix)
                     for _ in range(trials)])

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=Path('baseline-rerun'));a.add_argument('--seed',type=int,default=20260928);args=a.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    rows=[]
    for k,ns,T in [(3,[5,10,20,40,60,80,100],400),(4,[5,10,20,30,40],400),(5,[5,10,15,20,25,30],400)]:
        for n in ns:
            v=sample(n,k,T,args.seed+k*1000+n);E=math.comb(n,k)*2**(1-math.comb(k,2))
            rows.append(dict(k=k,n=n,trials=T,minimum=int(v.min()),maximum=int(v.max()),mean=float(v.mean()),theory=E,ratio=float(v.mean()/E),presence=int(np.count_nonzero(v)),zeros=int(np.count_nonzero(v==0))))
            print('growth',k,n,flush=True)
    for k,ns,T in [(3,[4,5,6],10000),(4,[8,9,10,11,12,13],5000),(5,[13,14,15,16,17],1500)]:
        for n in ns:
            v=sample(n,k,T,args.seed+100000+k*1000+n);E=math.comb(n,k)*2**(1-math.comb(k,2))
            rows.append(dict(k=k,n=n,trials=T,minimum=int(v.min()),maximum=int(v.max()),mean=float(v.mean()),theory=E,ratio=float(v.mean()/E),presence=int(np.count_nonzero(v)),zeros=int(np.count_nonzero(v==0)),kind='threshold'))
            print('threshold',k,n,flush=True)
    (args.out/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
    (args.out/'metadata.json').write_text(json.dumps(dict(seed=args.seed,python=platform.python_version(),numpy=np.__version__,note='Independent rerun of the revised paper baseline; the first draft’s original source is unavailable.'),indent=2)+'\n')
if __name__=='__main__':main()
