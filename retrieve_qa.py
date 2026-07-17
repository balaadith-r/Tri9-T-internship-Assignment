import argparse
from pprint import pprint

from services.retrieval_service import RetrievalService


def main():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--selection",
        type=int,
        help="Selection ID",
    )

    group.add_argument(
        "--node",
        type=int,
        help="Node ID",
    )

    group.add_argument(
        "--history",
        type=int,
        help="Selection ID for history",
    )

    args = parser.parse_args()

    service = RetrievalService()

    if args.selection:
        result = service.get_latest(args.selection)

    elif args.history:
        result = service.get_history(args.history)

    else:
        result = service.get_by_node_id(args.node)

    pprint(result)


if __name__ == "__main__":
    main()