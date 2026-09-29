"""Try three public PySAT-backed solvers on the same K13 CNF."""
import argparse,csv,json,math,platform
from pathlib import Path
from sat_compare import sat_search
from experiments import present
import numpy as np

def main():
    a=argparse.ArgumentParser();a.add_argument('--n',type=int,default=13);a.add_argument('--seconds',type=float,default=5);a.add_argument('--out',type=Path,default=Path('output/solver_survey'));args=a.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    rows=[];models={}
    for name,label in [('m22','Minisat22'),('g3','Glucose3'),('g4','Glucose4')]:
        status,bits,elapsed=sat_search(args.n,args.seconds,name)
        if bits is not None:
            assert len(bits)==math.comb(args.n,2) and not present(np.asarray(bits,dtype=np.uint8),args.n,4)
            models[label]=bits
        rows.append(dict(solver=label,pysat_name=name,n=args.n,k=4,variables=math.comb(args.n,2),clauses=2*math.comb(args.n,4),status=status,wall_seconds=round(elapsed,6)))
    with (args.out/'solver_survey.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    (args.out/'verified_models.json').write_text(json.dumps(models,indent=2)+'\n')
    (args.out/'metadata.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,time_budget=args.seconds,n=args.n,note='One run per deterministic solver. Runtime includes process startup and CNF construction. Timeout is unresolved.'),indent=2)+'\n')
    print(rows)
if __name__=='__main__':main()
