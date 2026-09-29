"""All random Ramsey experiments. See README for profiles and interpretation."""
import argparse, csv, itertools, json, math, platform, time
from pathlib import Path
import numpy as np

def clique_indices(n,k):
    if math.comb(n,k)*math.comb(k,2)>10_000_000: raise MemoryError('10-million index entry cap')
    def edge(a,b):return a*n-a*(a+1)//2+b-a-1
    return np.array([[edge(a,b) for a,b in itertools.combinations(s,2)] for s in itertools.combinations(range(n),k)],dtype=np.int32)

def count(bits,ix):
    x=bits[ix]
    return int(np.count_nonzero(np.all(x==0,axis=1)|np.all(x==1,axis=1)))

def present(bits,n,k):
    adj=[[0]*n for _ in range(2)]; i=0
    for a in range(n):
        for b in range(a+1,n):
            c=int(bits[i]);i+=1;adj[c][a]|=1<<b;adj[c][b]|=1<<a
    def find(A,candidates,need):
        if need==0:return True
        while candidates.bit_count()>=need:
            bit=candidates&-candidates;v=bit.bit_length()-1;candidates^=bit
            if find(A,candidates&A[v],need-1):return True
        return False
    return find(adj[0],(1<<n)-1,k) or find(adj[1],(1<<n)-1,k)

def batch(n,k,T,seed,mode,deadline=None,min_trials=0):
    rng=np.random.default_rng(seed);ix=clique_indices(n,k) if mode=='count' else None
    values=[];witness=None
    for j in range(T):
        if j>=min_trials and deadline and time.monotonic()>=deadline:break
        bits=rng.integers(0,2,size=math.comb(n,2),dtype=np.uint8)
        x=count(bits,ix) if ix is not None else int(present(bits,n,k))
        values.append(x)
        if not x and witness is None:witness=bits.tolist()
    return values,witness

def save(path,rows):
    if not rows:return
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)

def main():
    a=argparse.ArgumentParser();a.add_argument('--profile',choices=['quick','full'],default='quick');a.add_argument('--out',type=Path,default=Path('output'));a.add_argument('--seed',type=int,default=20260928);a.add_argument('--max-n-growth',type=int,default=100);a.add_argument('--max-n-threshold',type=int,default=55);a.add_argument('--max-k-threshold',type=int,default=7);args=a.parse_args()
    args.out.mkdir(parents=True,exist_ok=True);quick=args.profile=='quick';gT,gLimit,pT,pLimit,zT=(100,15,400,12,2000) if quick else (2000,600,3000,300,50000)
    growth=[];threshold=[];avoid=[];witnesses=[];start=time.monotonic()
    for k in (3,4,5):
        for n in range(5,args.max_n_growth+1):
            if math.comb(n,k)*math.comb(k,2)>10_000_000:break
            t=time.monotonic();v,_=batch(n,k,gT,args.seed+100000*k+n,'count',t+gLimit,min(25,gT))
            if len(v)<gT:break
            E=math.comb(n,k)*2**(1-math.comb(k,2));mean=sum(v)/len(v)
            growth.append(dict(k=k,n=n,trials=len(v),minimum=min(v),maximum=max(v),mean=mean,theory=E,ratio=mean/E,zeros=v.count(0),seconds=round(time.monotonic()-t,3)))
            save(args.out/'growth.csv',growth)
            if time.monotonic()-t>=gLimit:break
        print('growth',k,'finished',flush=True)
    for k in range(3,args.max_k_threshold+1):
        t=time.monotonic();cross=False
        for n in range(k,args.max_n_threshold+1):
            remaining=pLimit-(time.monotonic()-t)
            if remaining<=0:break
            v,_=batch(n,k,pT,args.seed+1000000*k+n,'presence',time.monotonic()+remaining,min(50,pT))
            if len(v)<pT:break
            hits=sum(v);threshold.append(dict(k=k,n=n,trials=len(v),present=hits,probability=hits/len(v),zeros=len(v)-hits,seconds=round(time.monotonic()-t,3)))
            save(args.out/'thresholds.csv',threshold)
            if hits/len(v)>=.9:cross=True;break
        print('threshold',k,'crossed' if cross else 'censored',flush=True)
    for k,lo,hi in ((3,4,6),(4,8,17)):
        for n in range(lo,hi+1):
            v,w=batch(n,k,zT,args.seed+10000000*k+n,'presence')
            avoid.append(dict(k=k,n=n,trials=len(v),zeros=len(v)-sum(v),probability_zero=(len(v)-sum(v))/len(v)))
            if w is not None:
                assert not present(np.asarray(w,dtype=np.uint8),n,k)
                witnesses.append(dict(k=k,n=n,edges_upper_triangle=w,seed=args.seed+10000000*k+n))
            save(args.out/'avoidance.csv',avoid)
    (args.out/'witnesses.json').write_text(json.dumps(witnesses,indent=2)+'\n')
    metadata=dict(profile=args.profile,seed=args.seed,growth_trials=gT,growth_seconds_per_n=gLimit,threshold_trials=pT,threshold_seconds_per_k=pLimit,avoidance_trials_per_n=zT,max_n_growth=args.max_n_growth,max_n_threshold=args.max_n_threshold,max_k_threshold=args.max_k_threshold,python=platform.python_version(),numpy=np.__version__,elapsed_seconds=round(time.monotonic()-start,3),note='Only complete batches are saved; a time or memory cap can censor a threshold.')
    (args.out/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps(metadata,indent=2),flush=True)
if __name__=='__main__':main()
