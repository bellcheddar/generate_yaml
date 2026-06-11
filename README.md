# generate_yaml.py

A command-line utility for generating Boltz-2 / co-folding input YAML files from a batch of candidate SMILES stored in a JSON file. Designed to work with the output format produced by generative chemistry runs (e.g. fragment-based screening, de novo design) and feed directly into a Boltz-style ModelCIF prediction pipeline.

---

## Overview

Given a JSON file containing a dictionary of candidate SMILES under a `"candidates"` key, `generate_yaml.py` interactively prompts for protein context and contact constraints, then writes one YAML file per selected candidate — ready to submit to Boltz-2 (or a compatible co-folding engine) for structure prediction with binding affinity estimation.

Each output YAML encodes:
- A single protein chain with user-supplied ID and sequence
- A ligand defined by cleaned SMILES
- A pocket constraint anchoring the ligand to a specified contact residue
- An affinity property block targeting the ligand

---

## Requirements

- Python 3.8+
- Standard library only (`argparse`, `json`, `re`, `pathlib`) — no additional dependencies

---

## Installation

```bash
git clone https://github.com/<your-org>/generate_yaml.git
cd generate_yaml
# No install step required — pure stdlib
```

---

## Usage

```bash
python generate_yaml.py <json_file>
```

### Example

```bash
python generate_yaml.py scratch_Baricitinib_sim.out.20260530_0219.json
```

The script will interactively prompt for:

| Prompt | Description | Example |
|---|---|---|
| `Protein ID` | Chain identifier used in the YAML | `A` |
| `Protein sequence` | Full single-letter amino acid sequence | `MGHHHHHHSSGVD...` |
| `Contact residue number` | Residue number defining the binding pocket | `1007` |
| `Output directory` | Path where YAML files will be written | `~/boltz_runs/baricitinib/` |
| `Candidate selection` | Which candidates to export (see below) | `1-25` or `all` |

---

## Candidate Selection Syntax

| Format | Description | Example |
|---|---|---|
| `all` | Export every candidate | `all` |
| `N` | A single candidate by 1-based index | `7` |
| `N-M` | An inclusive range | `1-25` |
| `N, M, ...` | Arbitrary comma-separated list | `1, 7, 17, 28, 31` |

Candidate numbering is **1-based** and follows the original key order in the JSON `"candidates"` dictionary.

---

## Output

Files are written to the specified output directory, named sequentially by candidate index:
