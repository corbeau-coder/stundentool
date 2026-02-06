import sys
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


    if args.purge:
        purge()

        
    try:
        graduation_checker(args.hours)
    except Exception as e:
        logger.error(
            f"Error initiating the data object\ninput value: {args.hours} \nException {str(e)}"
        )
        sys.exit(0)

    # arguments: read, change, store, init
    return


def graduation_checker(value_to_check: float):
    if not (isinstance(value_to_check, float)):
        logger.error(f"Error handling hour input {value_to_check}: wrong input type")
        raise TypeError("Error: input has wrong type, expected float ( 12.34 )")
    elif not (value_to_check % 0.25 == 0):
        logger.error(
            f"Error handling hour input {value_to_check}: valid float but invalid graduated"
        )
        raise ValueError("Error: Value given is not chosen correctly")
    else:
        return


def purge():
    logger.warning("WARNING: you ask for purging all data - data will be completly lost! Please confirm by typing y, any other character or string will abort: ")
    input_data = input("prees y to continue, anything else to aboort:")
    logger.debug("Input given: {input_data}")
    if (input_data and input_data == len(input_data) * input_data[0] and input_data == "y"):
        logger.info("Purging requested, starting routine deleting db")
        delete_db()
        sys.exit(0)
    else:
        logger.info("Purge aborted, exiting program")
        sys.exit(0)



if __name__ == "__main__":
    main()
