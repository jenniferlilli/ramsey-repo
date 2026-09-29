"""Project One distributions of monochromatic K3 and K4 counts."""
import argparse,csv,json,math,platform
from collections import Counter
from pathlib import Path
import numpy as np
from experiments import clique_indices,count

def write(path,rows):
    if not rows:return
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--out',type=Path,default=Path('output/distributions'))
    a.add_argument('--trials',type=int,default=100)
    a.add_argument('--seed',type=int,default=20260928)
    a.add_argument('--n',type=int,help='Optional single graph order')
    a.add_argument('--k',type=int,help='Optional clique order; requires --n')
    args=a.parse_args()
    if args.trials<1 or (args.n is None)!=(args.k is None):a.error('Positive trials and both --n/--k are required for single-point mode')
    grid=[(args.n,args.k)] if args.n is not None else [(n,3) for n in range(5,11)]+[(n,4) for n in range(10,26)]
    args.out.mkdir(parents=True,exist_ok=True)
    frequencies=[];summary=[]
    for n,k in grid:
        if not 2<=k<=n:a.error('Require 2 <= k <= n')
        rng=np.random.default_rng(args.seed+10000*k+n);ix=clique_indices(n,k)
        values=[count(rng.integers(0,2,size=math.comb(n,2),dtype=np.uint8),ix) for _ in range(args.trials)]
        freq=Counter(values);highest=max(freq.values());modes=sorted(v for v,f in freq.items() if f==highest)
        for value,f in sorted(freq.items()):
            frequencies.append(dict(k=k,n=n,monochromatic_count=value,frequency=f,trials=args.trials))
        E=math.comb(n,k)*2**(1-math.comb(k,2))
        summary.append(dict(k=k,n=n,trials=args.trials,modes=';'.join(map(str,modes)),mode_frequency=highest,minimum=min(values),maximum=max(values),mean=sum(values)/len(values),exact_expectation=E,zeros=freq[0]))
        print('distribution',k,n,'mode',modes,flush=True)
    write(args.out/'frequencies.csv',frequencies);write(args.out/'summary.csv',summary)
    (args.out/'metadata.json').write_text(json.dumps(dict(seed=args.seed,trials=args.trials,grid=grid,python=platform.python_version(),numpy=np.__version__,note='Modes and minima are sample statistics, not universal extremal results.'),indent=2)+'\n')
if __name__=='__main__':main()
