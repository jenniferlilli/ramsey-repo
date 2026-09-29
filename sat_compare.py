"""Compare uniform sampling with SAT for K4-avoiding two-colorings.

Each method gets the same wall-clock search budget per run. The CNF uses one
variable per edge and two clauses per four-vertex subset. SAT models are checked
independently before recording them as witnesses.
"""
import argparse,csv,itertools,json,math,multiprocessing as mp,platform,time
from pathlib import Path
import numpy as np
from experiments import present

def edge(n,a,b):return a*n-a*(a+1)//2+b-a

def clauses(n,k=4):
    for vertices in itertools.combinations(range(n),k):
        vs=[edge(n,a,b) for a,b in itertools.combinations(vertices,2)]
        yield vs
        yield [-v for v in vs]

def sat_worker(n,queue,solver_name):
    from pysat.solvers import Solver
    start=time.monotonic()
    with Solver(name=solver_name,bootstrap_with=clauses(n)) as s:
        status=s.solve()
        model=s.get_model() if status else None
    queue.put(dict(status='sat' if status else 'unsat',model=model,seconds=time.monotonic()-start))

def sat_search(n,limit,solver_name='m22'):
    ctx=mp.get_context('spawn');q=ctx.Queue();p=ctx.Process(target=sat_worker,args=(n,q,solver_name));start=time.monotonic();p.start();p.join(limit)
    if p.is_alive():
        p.terminate();p.join();return 'timeout',None,time.monotonic()-start
    if p.exitcode!=0 or q.empty():raise RuntimeError(f'SAT worker exited {p.exitcode}')
    result=q.get();status=result['status'];model=result['model'];bits=None
    if status=='sat':
        positives=set(v for v in model if v>0)
        bits=[int(i+1 in positives) for i in range(math.comb(n,2))]
        if present(np.asarray(bits,dtype=np.uint8),n,4):raise AssertionError('Invalid SAT witness')
    return status,bits,time.monotonic()-start

def random_search(n,limit,seed):
    rng=np.random.default_rng(seed);start=time.monotonic();tries=0
    while time.monotonic()-start<limit or tries==0:
        bits=rng.integers(0,2,size=math.comb(n,2),dtype=np.uint8);tries+=1
        if not present(bits,n,4):return 'found',bits.tolist(),time.monotonic()-start,tries
    return 'timeout',None,time.monotonic()-start,tries

def save(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    a=argparse.ArgumentParser();a.add_argument('--min-n',type=int,default=10);a.add_argument('--max-n',type=int,default=17);a.add_argument('--repeats',type=int,default=5);a.add_argument('--seconds',type=float,default=5);a.add_argument('--seed',type=int,default=20260928);a.add_argument('--solver',choices=['m22','g3','g4'],default='m22');a.add_argument('--out',type=Path,default=Path('comparison'));args=a.parse_args()
    if args.min_n<4 or args.max_n<args.min_n or args.repeats<1 or args.seconds<=0:a.error('Invalid range, repeats or time budget')
    args.out.mkdir(parents=True,exist_ok=True);rows=[];witnesses=[]
    for n in range(args.min_n,args.max_n+1):
        # Repeated SAT solves are deterministic with this solver and CNF order.
        # Report one SAT solve per n; random sampling has independent repeats.
        status,bits,elapsed=sat_search(n,args.seconds,args.solver)
        rows.append(dict(method='SAT',n=n,repeat=0,status=status,seconds=round(elapsed,6),trials='',seed='',variables=math.comb(n,2),clauses=2*math.comb(n,4)))
        if bits is not None:witnesses.append(dict(method='SAT',n=n,repeat=0,edges_upper_triangle=bits))
        for rep in range(args.repeats):
            seed=args.seed+1000*n+rep
            status,bits,elapsed,tries=random_search(n,args.seconds,seed)
            rows.append(dict(method='uniform_random',n=n,repeat=rep,status=status,seconds=round(elapsed,6),trials=tries,seed=seed,variables=math.comb(n,2),clauses=2*math.comb(n,4)))
            if bits is not None:witnesses.append(dict(method='uniform_random',n=n,repeat=rep,edges_upper_triangle=bits))
        save(args.out/'comparison.csv',rows)
        (args.out/'witnesses.json').write_text(json.dumps(witnesses,indent=2)+'\n')
        print(n,status,'SAT:',rows[-(args.repeats+1)]['status'],flush=True)
    from pysat import __version__ as pysat_version
    metadata=dict(seed=args.seed,repeats=args.repeats,seconds_per_run=args.seconds,min_n=args.min_n,max_n=args.max_n,python=platform.python_version(),numpy=np.__version__,pysat=pysat_version,solver=args.solver,note='SAT run once per n (deterministic CNF/solver); random independent repeats. Timeout means unresolved, not UNSAT. CNF creation occurs within SAT budget; random generator initialization occurs before its budget.')
    (args.out/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
if __name__=='__main__':main()
