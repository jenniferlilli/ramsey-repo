# Random Ramsey experiments

Reproducible code for independent red/blue edge colorings of complete graphs. Implements the [UMD final task list](https://www.cs.umd.edu/~gasarch/HSPROJ26/NRAMSEY/final-todo.pdf): sampled min/max/mean counts for K3–K5, 90% occurrence crossings for K3–K7 (as resources permit), and searches for avoiding colorings for K3/K4. The original report's earlier source and raw trials were unavailable; its numbers cannot be reconstructed by this code.

## Run

With Python 3.10+ in this directory:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python check.py
python experiments.py --profile quick --out output
python plot.py --input output
```

On Windows activate with `.venv\\Scripts\\activate`. Quick uses 100 count trials per n, 400 probability trials per n, 2,000 avoidance trials per n, 15 seconds per growth n and 12 seconds per threshold k. It is a smoke run. For the project brief's budgets:

```sh
python experiments.py --profile full --out output-full
python plot.py --input output-full
```

Full uses 2,000 count trials per n and 600 seconds per growth n; 3,000 probability trials per n and 300 seconds per threshold k; 50,000 avoidance trials per n. It can take hours. `--max-n-growth`, `--max-n-threshold`, and `--max-k-threshold` cap the search. The count index has a 10-million entry memory cap. Only complete trial batches enter the saved tables. A threshold not reached before a cap or time budget is censored, not known to be higher. At each n the first sample fraction at least 0.9 is an empirical crossing, not a mathematically certified 0.9 probability.

A bounded demonstration is included in `example-output/` (100 count trials per n through n=25, 400 probability trials per n through n=32 and k=6). These are not the full-profile research results. Results in the chosen output directory: `growth.csv`, `thresholds.csv`, `avoidance.csv`, `witnesses.json`, `metadata.json` and eight figures in `figures/`. `witnesses.json` records the first zero-count coloring per tested point in upper-triangle edge order (0,1), (0,2), …, (n−2,n−1), verified by an independent bitset detector. A recorded witness proves R(k,k)>n; failing to find one gives no upper bound.

The expectation is exactly C(n,k)·2^(1−C(k,2)). Min/max are **sample extrema**. Colorings are independent across trials, but clique indicators within one coloring are dependent. Interpret probabilities with binomial sampling uncertainty and account for exploratory n selection. Reproducible graphs alone do not establish a novel result or publication acceptance.

The existing `results.json` is a separate fixed-grid rerun used in the revised report. Its seed schedule and grids differ from `experiments.py`; keep its provenance separate. `check.py` cross-checks the count and bitset algorithms and exhaustively verifies that 12 of 1,024 colorings of K5 avoid a monochromatic triangle.

## Project One plus Project Three: targeted search comparison

`experiments.py` is the original random-coloring baseline. `sat_compare.py` adds Project Three: each edge is one Boolean variable (true=blue). For each four-vertex subset with six edge variables, a positive clause excludes an all-red K4 and a negative clause excludes an all-blue K4. There are C(n,2) variables and 2C(n,4) clauses. A SAT model is independently checked with the bitset clique detector before it is saved. See the project brief and [PySAT solver API](https://pysathq.github.io/docs/api/solvers.html).

```sh
python sat_compare.py --min-n 10 --max-n 17 --repeats 20 --seconds 5 --out comparison-full
python plot_compare.py --input comparison-full
```

At each n, one deterministic Minisat22 solve and the requested number of independent random samples receive the same wall-clock time allowance. SAT process startup and CNF building are included in its budget. The random search stops at its first verified coloring or its deadline. SAT has one run per n because identical formula and solver order make repeats redundant; its plotted 0/1 status is not a statistical success probability. A timeout is **unresolved**, never UNSAT. The example pilot in `example-comparison/` uses 3 random repeats and only 0.5 seconds at each n. Do not use it to claim a robust speedup. For publication-quality comparison, run more seeds and budgets, record hardware, and compare against established SAT/heuristic approaches. The methodology of encoding Ramsey colorings in SAT is established; this code does not claim it as an invention.

## Paper

`Random_Ramsey_SAT_Extension.docx` builds on the supplied random Ramsey report. Sections 1–6 present the random-coloring baseline, and Section 7 introduces the SAT comparison with its bounded pilot. The companion full benchmark command above has **not** been run; update the manuscript with full results and uncertainty before submission.

## Reproduce the paper figures exactly

Run `python paper_figures.py` from this directory. Figure 1 is regenerated from the included fixed-grid `results.json`; Figure 2 from the included `example-comparison/comparison.csv`. The resulting PNG and PDF files appear in `paper-figures/`. This redraws the plotted data without resampling. The text tables in the paper also derive from `results.json` and the pilot CSV. `plot.py` and `plot_compare.py` instead plot a *new* run's CSV files, so new random runs will not match the manuscript's values exactly.

## Rerun, then redraw (instead of merely replotting stored data)

```sh
python rerun_paper_baseline.py --out baseline-rerun
python sat_compare.py --min-n 10 --max-n 17 --repeats 20 --seconds 5 --out comparison-full
python paper_figures.py --baseline-json baseline-rerun/results.json --comparison-csv comparison-full/comparison.csv --output new-figures
```

The first command actually regenerates the revised paper's 400-trial growth grids and dedicated 10,000/5,000/1,500-trial probability grids using their published seed schedule. The second actually generates a *new, longer* SAT/random benchmark. The third plots the freshly produced data, saving `new-figures/figure1-growth.png` and `figure2-comparison.png` (also PDF). If NumPy's random generator implementation differs by version, values may differ; the new metadata files record the environment. The fixed-grid baseline is a separate, independently created run from the first attached draft, whose source and seeds were absent. If you report newly generated values, revise the manuscript's tables, descriptions, and figure captions rather than swapping only the images.

## One-command fresh reproduction of Projects One and Three

```sh
python run_all.py --profile quick --out fresh-quick
python run_all.py --profile full --out fresh-full
```

These commands start from scratch and create every output under the specified directory. `quick` verifies the pipeline; `full` can take hours. Neither reads the paper's `results.json` or pilot CSV. The output contains:

- `distributions/`: 100 or 2,000 fresh colorings per n for K3 in K5–K10 and K4 in K10–K25, frequency tables, modes, means, minima/maxima, exact expected counts, and distribution plots.
- `monte_carlo/`: fresh K3/K4/K5 growth samples; presence probability searches for k=3–7 as far as limits permit; random avoiding searches for K3 and K4; separately checked witness bitstrings; four figure pairs. All time-censored searches are marked by their complete last row and the runtime configuration.
- `sat/`: a standard DIMACS CNF example for a K13 coloring with no monochromatic K4, PySAT Minisat22 comparison against uniform sampling on K10–K17, verified witnesses, and a comparison figure. `timeout` is unresolved, not a proof of nonexistence.
- `run_manifest.json`: the run settings and elapsed time. Per-experiment metadata includes Python and dependency versions.

The data from this command are independent of the supplied original draft and the revised paper's pilot. A paper based on `fresh-full` must report its actual outputs, not reuse the old numerical text. Sampled minimum counts cannot prove the project's “always at least” claims; proving those requires a separate mathematical argument or exhaustive verified search.

Project Three's solver survey also tries PySAT's Minisat22, Glucose3, and Glucose4 on the same K13 instance; see `sat/solver_survey/`. Their input is DIMACS CNF (header `p cnf variables clauses`, signed integer literals ending in 0), exported by `export_cnf.py`. The survey records one deterministic run per solver, its wall time, and independently verified models. It is an introductory comparison, not a claim that any solver is generally fastest. To survey a different size: `python solver_survey.py --n 13 --seconds 5 --out solver-results`.

On Windows, use `py` in place of `python` in these commands. The checked-in `example-fresh-quick/` is one complete quick run for inspection. Delete or choose a new `--out` directory for a fresh independent run. The full profile was implemented and documented but has not been executed for the accompanying paper.
