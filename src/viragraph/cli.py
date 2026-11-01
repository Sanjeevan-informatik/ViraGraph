"""Command-line interface for local sequence analysis."""
import argparse
import json
from pathlib import Path
from .core import read_fasta, summary
from .graph import build_graph

def main() -> None:
    parser = argparse.ArgumentParser(prog="viragraph")
    subs = parser.add_subparsers(dest="command", required=True)
    for name in ("summary", "graph"):
        sub = subs.add_parser(name)
        sub.add_argument("fasta")
        if name == "graph":
            sub.add_argument("--output")
    args = parser.parse_args()
    records = read_fasta(args.fasta)
    result = summary(records) if args.command == "summary" else build_graph(records)
    data = json.dumps(result, indent=2)
    if getattr(args, "output", None):
        Path(args.output).write_text(data + "\n", encoding="utf-8")
    else:
        print(data)

if __name__ == "__main__":
    main()
