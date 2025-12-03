import argparse

""""
Takes care of starting the process by running thought terminal at the backend root
python -m app.tokenization.cli 

"""

from app.tokenization.pipeline import run_tokenization


def main():
    parser = argparse.ArgumentParser(
        description="Tokenize/label all IKEA hacks in MongoDB with LLM."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Max number of documents to process (default: no limit).",
    )
    args = parser.parse_args()

    run_tokenization(limit=args.limit)


if __name__ == "__main__":
    main()
