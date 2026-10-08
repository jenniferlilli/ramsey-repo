# Random Ramsey Theory

**Expected Clique Counts, Probability Crossings, and Verified Avoiding Colorings**

A reproducible computational study of random red-blue colorings of complete graphs, focusing on monochromatic clique counts, empirical probability crossings, Ramsey-avoiding colorings, and SAT-based searches.

## Project Scope

- Monochromatic \(K_3\), \(K_4\), and \(K_5\) counts and distributions
- Empirical 90% occurrence crossings for \(K_3\)–\(K_7\)
- Random searches for Ramsey-avoiding colorings
- SAT encoding and search for monochromatic \(K_4\)-avoiding colorings
- Random-search vs. SAT comparisons
- Independent verification of computed results and witnesses

The project implements the UMD Ramsey Theory task list. It compares random behavior with targeted SAT search under stated computational budgets and does not claim new Ramsey bounds or a general SAT-solver ranking.

## Main Results

Sample means closely matched the exact expectation

\[
E[X(n,k)] = \binom{n}{k}2^{1-\binom{k}{2}}.
\]

The first tested sizes reaching an observed 90% monochromatic-clique occurrence were:

| Clique | \(n\) |
|--------|------:|
| \(K_3\) | 5 |
| \(K_4\) | 9 |
| \(K_5\) | 15 |
| \(K_6\) | 24 |
| \(K_7\) | 36 |

In the five-second SAT comparison, random search succeeded in **20/20 runs at \(n=10\)–11**, **9/20 at \(n=12\)**, and **0/20 at \(n=13\)–17**. SAT produced independently verified \(K_4\)-avoiding colorings for \(n=10\)–17.

These results are empirical and budget-specific. A failed or timed-out search does not prove that an avoiding coloring does not exist.

## Requirements

- Python 3.10+
- `numpy>=1.24,<3`
- `matplotlib>=3.7,<4`
- `python-sat>=1.8.dev13,<2`

Install all dependencies with:

```bash
python -m pip install -r requirements.txt
```

On Windows, use `py` instead of `python`.

## Quick Start

Run the verification checks:

```bash
python check.py
```

Run the quick experimental profile:

```bash
python experiments.py --profile quick --out output
```

Generate the corresponding plots:

```bash
python plot.py --input output
```

The quick profile is a reduced smoke test. For the larger study:

```bash
python experiments.py --profile full --out output-full
python plot.py --input output-full
```

> **Note:** The full profile can take hours.

## Core Files

### `experiments.py`

Main Monte Carlo engine. Generates clique-count, probability, avoidance, witness, and metadata results.

### `distributions.py`

Generates \(K_3\) and \(K_4\) count distributions and summary statistics.

### `check.py`

Cross-checks the counting and detection algorithms and exhaustively verifies that **12 of the 1,024 red-blue colorings of \(K_5\) avoid a monochromatic triangle**.

### `run_all.py`

Runs the main random and SAT workflows from one command:

```bash
python run_all.py --profile quick --out fresh-quick
```

Use `--profile full` for the full study.

## SAT Experiments

### `sat_compare.py`

Compares uniform random search with MiniSat22 for \(K_4\)-avoiding colorings.

Each edge is represented by a Boolean variable. Each 4-vertex subset contributes two clauses:

- one excluding an all-red \(K_4\)
- one excluding an all-blue \(K_4\)

Example:

```bash
python sat_compare.py --min-n 10 --max-n 17 --repeats 20 --seconds 5 --out comparison-full
```

### `export_cnf.py`

Exports Ramsey-avoidance problems as standard DIMACS CNF files.

### `solver_survey.py`

Tests MiniSat22, Glucose3, and Glucose4 on the same SAT instance and independently verifies returned colorings.

## Plotting

- `plot.py` — growth, expectation-ratio, threshold, and avoidance plots
- `plot_distributions.py` — \(K_3\)/\(K_4\) distributions
- `plot_compare.py` — random vs. SAT results
- `paper_figures.py` — recreates figures from archived data

## Outputs

Main experiments produce:

```text
growth.csv
thresholds.csv
avoidance.csv
witnesses.json
metadata.json
figures/
```

`witnesses.json` stores independently verified avoiding colorings, while `metadata.json` records seeds, trial counts, limits, and software information.

The default seed is **20260928**.

## Reproducibility Notes

Simulation results are empirical.

- Sample extrema are **not** mathematical bounds.
- Observed 90% crossings are **not** proven thresholds.
- Zero random successes do **not** prove nonexistence.
- A SAT timeout means the problem was unresolved within the time limit, **not** that the instance is UNSAT.

The archived paper results and fresh experimental runs use separate data and seed schedules.

The full profile has **not** been executed for the accompanying paper.

## Citation

**Random Ramsey Theory: Expected Clique Counts, Probability Crossings, and Verified Avoiding Colorings.** Revised research report, September 2026.

Repository: `https://github.com/jenniferlilli/ramsey-repo`

## References

1. William Gasarch, *HS PROJ 2026 New Ramsey*, University of Maryland.
2. Stanisław P. Radziszowski, *Small Ramsey Numbers*, *Electronic Journal of Combinatorics*, Dynamic Survey DS1.
3. PySAT Documentation and Solver API.
