"""Recreate Figures 1 and 2 of Random_Ramsey_SAT_Extension.docx.

Figure 1 uses the fixed-grid results.json data. Figure 2 uses the bounded
pilot in example-comparison/comparison.csv. No simulation is rerun here.
"""
import argparse,csv,json
from collections import defaultdict
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--baseline-json',type=Path,default=ROOT/'results.json')
    ap.add_argument('--comparison-csv',type=Path,default=ROOT/'example-comparison'/'comparison.csv')
    ap.add_argument('--output',type=Path,default=ROOT/'paper-figures')
    args=ap.parse_args();OUT=args.output;OUT.mkdir(parents=True,exist_ok=True)
    rows=json.loads(args.baseline_json.read_text())
    fig,axs=plt.subplots(1,3,figsize=(10,2.7))
    for ax,k in zip(axs,(3,4,5)):
        rr=[r for r in rows if r['k']==k and not r.get('kind')]
        ax.plot([r['n'] for r in rr],[r['mean'] for r in rr],'o-',label='sample mean')
        ax.plot([r['n'] for r in rr],[r['theory'] for r in rr],'--',label='exact expectation')
        ax.set_title(f'K{k}');ax.set_xlabel('n');ax.set_ylabel('count');ax.grid(alpha=.2)
    axs[0].legend(fontsize=7);fig.tight_layout()
    fig.savefig(OUT/'figure1-growth.png',dpi=180);fig.savefig(OUT/'figure1-growth.pdf');plt.close(fig)
    with args.comparison_csv.open(newline='') as f:comparison=list(csv.DictReader(f))
    grouped=defaultdict(list)
    for r in comparison:grouped[(r['method'],int(r['n']))].append(r)
    ns=sorted({int(r['n']) for r in comparison});fig,ax=plt.subplots(figsize=(7,4))
    for method,label,marker in [('uniform_random','Uniform random','o'),('SAT','SAT solver','s')]:
        ys=[sum(r['status'] in ('found','sat') for r in grouped[(method,n)])/len(grouped[(method,n)]) for n in ns]
        ax.plot(ns,ys,marker=marker,label=label)
    ax.set(xlabel='Number of vertices n',ylabel='Fraction of runs finding a verified coloring',ylim=(-.05,1.05),xticks=ns)
    ax.legend();ax.spines[['top','right']].set_visible(False);fig.tight_layout()
    fig.savefig(OUT/'figure2-comparison.png',dpi=300);fig.savefig(OUT/'figure2-comparison.pdf');plt.close(fig)
    print('Regenerated paper Figures 1 and 2 in',OUT)
if __name__=='__main__':main()
