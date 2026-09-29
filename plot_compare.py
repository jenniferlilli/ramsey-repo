"""Visualize success within the benchmark budget; never treat a timeout as UNSAT."""
import argparse,csv
from collections import defaultdict
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    a=argparse.ArgumentParser();a.add_argument('--input',type=Path,default=Path('comparison'));a.add_argument('--output',type=Path);args=a.parse_args();out=args.output or args.input;out.mkdir(parents=True,exist_ok=True)
    with (args.input/'comparison.csv').open(newline='') as f:rows=list(csv.DictReader(f))
    groups=defaultdict(list)
    for r in rows:groups[(r['method'],int(r['n']))].append(r)
    ns=sorted({int(r['n']) for r in rows});fig,ax=plt.subplots(figsize=(7,4))
    for method,label,marker in [('uniform_random','Uniform random','o'),('SAT','SAT solver','s')]:
        ys=[sum(r['status'] in ('found','sat') for r in groups[(method,n)])/len(groups[(method,n)]) for n in ns]
        ax.plot(ns,ys,marker=marker,label=label)
    ax.set(xlabel='Number of vertices n',ylabel='Fraction of runs finding a verified coloring',ylim=(-.05,1.05),xticks=ns)
    ax.legend();ax.spines[['top','right']].set_visible(False);fig.tight_layout()
    fig.savefig(out/'comparison.png',dpi=300);fig.savefig(out/'comparison.pdf');plt.close(fig)
    print('Saved comparison figures')
if __name__=='__main__':main()
