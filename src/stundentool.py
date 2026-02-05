import argparse
from loguru import logger


def main():
    parser = argparse.ArgumentParser(
        prog="stundentool",
        description="memorizing the hours scraped of off last years budget overhang",
        epilog="written with fun for fun",
    )

    parser.add_argument(
        "hours",
        type=float,
        help="time to scraped of the overhang budget. Schema HOURS.MINUTES - only 4 values are allowed for minutes: 00,25,50,75 reflecting that we usually round costs in 15 minute graduation",
    )
    parser.add_argument(
        "--purge",
        help="will purge the db and everything else - afterwards you have an fresh initiated instance of",
        action="store_true",
    )
    parser.add_argument(
        "--recal", help="recalculate the hours scraped off", action="store_true"
    )
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()
    if args.verbose:
        logger.level("DEBUG")
    else:
        logger.level("INFO")

    # arguments: read, change, store, init
    return


if __name__ == "__main__":
    main()
