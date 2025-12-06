import argparse
import json
import sys
from .core import SmallRAG


def main(argv=None):
    parser = argparse.ArgumentParser(prog="smallrag-cli")
    parser.add_argument("--db", default="smallrag.db")
    sub = parser.add_subparsers(dest="cmd")

    add = sub.add_parser("add")
    add.add_argument("text")
    add.add_argument("--meta", type=str, help="JSON metadata")

    q = sub.add_parser("query")
    q.add_argument("text")
    q.add_argument("--k", type=int, default=5)

    exp = sub.add_parser("export")
    exp.add_argument("path")

    im = sub.add_parser("import")
    im.add_argument("path")

    args = parser.parse_args(argv)
    rag = SmallRAG(args.db)

    # CLI uses a dumb embedder until user sets one programmatically
    rag.set_embedder(lambda t: [float(ord(c) % 255) for c in t[:64]])

    if args.cmd == "add":
        meta = json.loads(args.meta) if args.meta else {}
        rag.add_document(args.text, metadata=meta)
        print("Inserted")
    elif args.cmd == "query":
        res = rag.query(args.text, top_k=args.k)
        print(json.dumps(res, indent=2))
    elif args.cmd == "export":
        rag.export_db(args.path)
        print("Exported")
    elif args.cmd == "import":
        rag.import_db(args.path)
        print("Imported")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()