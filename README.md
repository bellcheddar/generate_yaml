# 📝 generate_yaml.py

> **From a JSON of candidate SMILES to a folder of Boltz-2 input YAMLs, in one prompt.**

![python](https://img.shields.io/badge/python-3.8+-3776AB?logo=python&logoColor=white) ![dependencies](https://img.shields.io/badge/dependencies-zero-00897B) ![output](https://img.shields.io/badge/output-Boltz--2%20YAML-467FF7) ![input](https://img.shields.io/badge/input-JSON%20SMILES-9b51e0) ![author](https://img.shields.io/badge/author-Marc%20C.%20Deller%2C%20D.Phil.-1C244B)

<table>
<tr>
<td>🌐 <b>Website</b></td><td><a href="https://marcdeller.com" target="_blank" rel="noopener noreferrer">marcdeller.com</a></td>
<td>✉️ <b>Contact</b></td><td><a href="mailto:marc@marcdeller.com">marc@marcdeller.com</a></td>
<td>🐙 <b>GitHub</b></td><td><a href="https://github.com/bellcheddar/generate_yaml" target="_blank" rel="noopener noreferrer">bellcheddar/generate_yaml</a></td>
</tr>
</table>

---

A command-line utility for generating Boltz-2 / co-folding input YAML files from a batch of candidate SMILES stored in a JSON file. Designed to work with the output format produced by generative chemistry runs (e.g. fragment-based screening, de novo design) and feed directly into a Boltz-style ModelCIF prediction pipeline.

Why it matters: generative chemistry runs spit out hundreds of candidate SMILES, but Boltz-2 wants one carefully structured YAML per compound, each pairing the ligand with a protein chain, a pocket constraint, and an affinity block. Hand-writing those is tedious and error-prone. generate_yaml.py reads the candidates straight from your JSON, prompts once for the protein context, and writes a clean, submission-ready YAML for every selected compound. It is useful for anyone bridging de novo design or fragment screening into a co-folding affinity pipeline: turn a screening output into a ready-to-run prediction batch in seconds, with stdlib-only portability and no dependencies to install.

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

---

## 👤 Author

**Marc C. Deller, D.Phil.**  
Structural biologist & drug discovery scientist  

<table>
<tr>
<td>🌐</td><td><a href="https://marcdeller.com" target="_blank" rel="noopener noreferrer">marcdeller.com</a></td>
<td>✉️</td><td><a href="mailto:marc@marcdeller.com">marc@marcdeller.com</a></td>
<td>🐙</td><td><a href="https://github.com/bellcheddar/generate_yaml" target="_blank" rel="noopener noreferrer">github.com/bellcheddar/generate_yaml</a></td>
</tr>
</table>
