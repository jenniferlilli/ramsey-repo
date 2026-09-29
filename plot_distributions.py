"""Generate probability-mass plots for the assigned K3 and K4 grids."""
import argparse,csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    a=argparse.ArgumentParser();a.add_argument('--input',type=Path,default=Path('output/distributions'));a.add_argument('--output',type=Path);args=a.parse_args();out=args.output or args.input/'figures';out.mkdir(parents=True,exist_ok=True)
    with (args.input/'frequencies.csv').open(newline='') as f:rows=list(csv.DictReader(f))
    for k,selected in [(3,[5,6,7,8,9,10]),(4,[10,13,17,21,25])]:
        fig,axs=plt.subplots(2,3,figsize=(11,6.5));axs=axs.flat
        for i,n in enumerate(selected):
            rr=[r for r in rows if int(r['k'])==k and int(r['n'])==n];ax=axs[i]
            if rr:
                ax.bar([int(r['monochromatic_count']) for r in rr],[int(r['frequency'])/int(r['trials']) for r in rr],width=max(.8,(max(int(r['monochromatic_count']) for r in rr)-min(int(r['monochromatic_count']) for r in rr))/35))
                ax.set(title=f'K{k} in K{n}',xlabel='Monochromatic cliques',ylabel='Sample fraction')
            else:ax.set_axis_off()
        for j in range(len(selected),6):axs[j].set_axis_off()
        fig.tight_layout();fig.savefig(out/f'K{k}-distributions.png',dpi=250);fig.savefig(out/f'K{k}-distributions.pdf');plt.close(fig)
    print('Wrote distribution figures to',out)
if __name__=='__main__':main()
