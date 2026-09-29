"""Write a standard DIMACS CNF for a two-color Ramsey-avoiding problem."""
import argparse,math
from pathlib import Path
from sat_compare import clauses

def main():
    a=argparse.ArgumentParser();a.add_argument('--n',type=int,default=13);a.add_argument('--k',type=int,default=4);a.add_argument('--out',type=Path,default=Path('output/K13_no_K4.cnf'));args=a.parse_args()
    if not 2<=args.k<=args.n:a.error('Require 2 <= k <= n')
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('w') as f:
        f.write('c variable i colors edge i blue iff true; edges ordered upper triangle\n')
        f.write(f'p cnf {math.comb(args.n,2)} {2*math.comb(args.n,args.k)}\n')
        for clause in clauses(args.n,args.k):f.write(' '.join(map(str,clause))+' 0\n')
    print(args.out)
if __name__=='__main__':main()
