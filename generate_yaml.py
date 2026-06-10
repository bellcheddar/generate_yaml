#!/usr/bin/env python3
#
# generate_yaml.py
#
# Usage:
#   python generate_yaml.py scratch_Baricitinib_sim.out.20260530_0219.json
#
# Prompt examples for candidate selection:
#   all
#   1
#   1-25
#   1, 7, 17, 28, 31, 41, 54, 73, 87, 116, 130, 148, 171, 187, 227, 249, 256
#
# Notes:
#   - Candidate numbering is 1-based and follows the original JSON order.
#   - Output filenames are derived directly from the candidate number:
#       candidate 1 -> J001.yaml
#       candidate 17 -> J017.yaml
#   - SMILES are cleaned by taking only the part before the first ".".

import argparse
import json
import re
from pathlib import Path


EXACT_TEMPLATE = """sequences:
  - protein:
      id: {protein_id}
      sequence: {sequence}
  - ligand:
      smiles: '{smiles}'
      id: {ligand_id}
constraints:
  - pocket:
      binder: {ligand_id}
      contacts: [[{protein_id}, {contact_number}]]
properties:
  - affinity:
      binder: {ligand_id}
"""


def prompt_nonempty(prompt_text: str) -> str:
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def clean_smiles(smiles: str) -> str:
    return smiles.split(".", 1)[0]


def parse_selection(selection: str, total: int):
    s = selection.strip().lower()

    if s == "all":
        return list(range(total))

    if re.fullmatch(r"\d+", s):
        idx = int(s)
        if idx < 1 or idx > total:
            raise ValueError(f"Selection {idx} is out of range. Valid range is 1-{total} or all.")
        return [idx - 1]

    m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", s)
    if m:
        start = int(m.group(1))
        end = int(m.group(2))
        if start < 1 or end < 1 or start > end or end > total:
            raise ValueError(f"Selection {start}-{end} is out of range. Valid range is 1-{total} or all.")
        return list(range(start - 1, end))

    parts = [p.strip() for p in s.split(",") if p.strip()]
    if len(parts) > 1:
        indices = []
        seen = set()
        for part in parts:
            if not re.fullmatch(r"\d+", part):
                raise ValueError(
                    f"Invalid selection item '{part}'. Use numbers separated by commas, a range like 1-25, or all."
                )
            idx = int(part)
            if idx < 1 or idx > total:
                raise ValueError(f"Selection {idx} is out of range. Valid range is 1-{total} or all.")
            zero_based = idx - 1
            if zero_based not in seen:
                indices.append(zero_based)
                seen.add(zero_based)
        return indices

    raise ValueError(
        "Invalid selection. Use all, a single number, a range like 1-25, or a comma-separated list like 1, 7, 17."
    )


def build_yaml_exact(
    protein_id: str,
    sequence: str,
    contact_number: str,
    ligand_id: str,
    smiles: str,
) -> str:
    return EXACT_TEMPLATE.format(
        protein_id=protein_id,
        sequence=sequence,
        contact_number=contact_number,
        ligand_id=ligand_id,
        smiles=smiles,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Generate sequential YAML files from candidate SMILES in a JSON file."
    )
    parser.add_argument("json_file", help="Path to the JSON file containing candidates")
    args = parser.parse_args()

    json_path = Path(args.json_file)
    if not json_path.is_file():
        raise FileNotFoundError(f"JSON file not found: {json_path}")

    with json_path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    candidates = data.get("candidates")
    if not isinstance(candidates, dict) or not candidates:
        raise ValueError("JSON file does not contain a non-empty 'candidates' object")

    protein_id = prompt_nonempty("Protein ID: ")
    sequence = prompt_nonempty("Protein sequence: ")
    contact_number = prompt_nonempty("Contact residue number: ")
    output_dir_input = prompt_nonempty("Output directory: ")
    selection_input = prompt_nonempty(
        "Candidate selection (all, 1, 1-25, or 1, 7, 17): "
    )

    output_dir = Path(output_dir_input).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    candidate_smiles = list(candidates.keys())
    selected_indices = parse_selection(selection_input, len(candidate_smiles))

    written_files = []

    for candidate_index in selected_indices:
        raw_smiles = candidate_smiles[candidate_index]
        ligand_id = f"J{candidate_index + 1:03d}"
        smiles = clean_smiles(raw_smiles)
        yaml_text = build_yaml_exact(
            protein_id=protein_id,
            sequence=sequence,
            contact_number=contact_number,
            ligand_id=ligand_id,
            smiles=smiles,
        )
        output_path = output_dir / f"{ligand_id}.yaml"
        output_path.write_text(yaml_text, encoding="utf-8")
        written_files.append(output_path.name)

    print(f"Wrote {len(written_files)} YAML files to {output_dir}")
    if written_files:
        print(f"First file: {written_files[0]}")
        print(f"Last file: {written_files[-1]}")


if __name__ == "__main__":
    main()
