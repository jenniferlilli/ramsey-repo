"""Render four figures from experiments.py CSV files as PNG and vector PDF."""
import argparse,csv
from collections import defaultdict
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def read(p):
    with p.open(newline='') as f:return [{k:float(v) for k,v in row.items()} for row in csv.DictReader(f)]
def save(fig,d,name):
    fig.tight_layout();fig.savefig(d/(name+'.png'),dpi=300);fig.savefig(d/(name+'.pdf'));plt.close(fig)
def grouped(rows):
    groups=defaultdict(list)
    for r in rows:groups[int(r['k'])].append(r)
    return groups
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,default=Path('output'));ap.add_argument('--output',type=Path);a=ap.parse_args();d=a.output or a.input/'figures';d.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    growth=grouped(read(a.input/'growth.csv'));prob=grouped(read(a.input/'thresholds.csv'));avoid=grouped(read(a.input/'avoidance.csv'))
    fig,axs=plt.subplots(1,3,figsize=(12,3.4))
    for ax,k in zip(axs,(3,4,5)):
        rr=growth[k];ns=[r['n'] for r in rr]
        ax.fill_between(ns,[r['minimum'] for r in rr],[r['maximum'] for r in rr],alpha=.22,label='Sample min–max')
        ax.plot(ns,[r['mean'] for r in rr],label='Sample mean')
        ax.plot(ns,[r['theory'] for r in rr],'--',label='Exact expectation')
        ax.set(title=f'Monochromatic K{k}',xlabel='Vertices n',ylabel='Clique count')
    axs[0].legend(fontsize=7);save(fig,d,'growth')
    fig,ax=plt.subplots(figsize=(6.5,4))
    for k,rr in growth.items():ax.plot([r['n'] for r in rr],[r['ratio'] for r in rr],'.-',label=f'K{k}')
    ax.axhline(1,color='black',ls='--',lw=.8);ax.set(xlabel='Vertices n',ylabel='Sample mean / exact expectation');ax.legend();save(fig,d,'mean_theory_ratio')
    fig,ax=plt.subplots(figsize=(6.5,4))
    for k,rr in prob.items():ax.plot([r['n'] for r in rr],[r['probability'] for r in rr],'.-',label=f'K{k}')
    ax.axhline(.9,color='black',ls='--',lw=.8);ax.set(xlabel='Vertices n',ylabel='Fraction containing a monochromatic clique',ylim=(-.02,1.03));ax.legend();save(fig,d,'thresholds')
    fig,ax=plt.subplots(figsize=(6.5,4))
    for k,rr in avoid.items():ax.plot([r['n'] for r in rr],[r['probability_zero'] for r in rr],'.-',label=f'K{k}')
    ax.set(xlabel='Vertices n',ylabel='Fraction avoiding a monochromatic clique',ylim=(-.02,1.03));ax.legend();save(fig,d,'avoidance')
    print('Saved four PNG and four PDF figures in',d)
if __name__=='__main__':main()
