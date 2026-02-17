import sys
import argparse
from modules.data.store_handler import store_handler
from loguru import logger
from modules.data.data_handler import data_object



def main():
    path = "stundentool.db"


    parser = argparse.ArgumentParser(
        prog="stundentool",
        description="memorizing the hours scraped of off last years budget overhang",
        epilog="written with fun for fun",
    )

    parser.add_argument(
        "[hours.minutes]",
        type=float,
        help="time to scraped of the overhang budget. Schema HOURS.MINUTES - only 4 values are allowed for minutes: 00,25,50,75 reflecting that we usually round costs in 15 minute graduation"
    )
    parser.add_argument(
        "--init",
        help="will initiate the db with the hour overhang budget to be scraped from. the budget has to be appended to that parameter in the format [hours.minutes]",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "--purge",
        help="will purge the db and everything else - afterwards you have an fresh initiated instance of",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "--status",
        help="shows status of hours entered in db",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "--add",
        help="adds a new entry - do not forget to enter [hours.minutes] as well.",
        action="store_true",
        default=False
    )
    """parser.add_argument(
        "--recal", help="recalculate the hours scraped off", action="store_true"
    )"""
    parser.add_argument("--verbose", action="store_true")
    

    args = parser.parse_args()
    

    if args.verbose:
        logger.level("DEBUG")
        logger.debug("Verbose logging configured")
    else:
        logger.level("INFO")
        logger.debug("Normal logging configured")

    logger.debug("Loading DB and checking state...")
    storage = store_handler(path)
    logger.debug(f" DB check returns {storage.db_status}. done")



    #scheme:
    #purge | init | add | status

    routing_value = args.purge << 3 | args.init << 2 | args.add << 1 | args.status
    logger.debug(f"Routing value is {routing_value}")
    match routing_value:
        case 1:
            #calc and print status
            sys.exit(0)
        case 2:
            if args.hours is not None:
                if (graduation_checker(args.hours)):
                    new_data = data_object(args.hours)
                    storage.write_one(new_data)
                    sys.exit(0)
                else:
                    sys.exit(1)
            else:
                logger.error("Error: empty hours.minutes argument, cannot add entry.")
                sys.exit(0)
        case 4:
            if args.hours is not None:
                if (graduation_checker(args.hours)):
                    storage.init(args.hours)
                    #RETURN falsch, es wird nicht richtig auf exceptions reagiert
                    sys.exit(0)
                else:
                    sys.exit(1)

            storage.init(args.hours)
        case 8:
            purge(storage, path)
        case _:
            logger.error("Error: check parameter set used - do not combine purge, init, status or add as parameters")
            sys.exit(0)

        
    

    # arguments: read, change, store, init
    return


def graduation_checker(value_to_check: float) -> bool:
    if not (isinstance(value_to_check, float)):
        logger.error(f"Error handling hour input {value_to_check}: wrong input type, expected float ( 12.34 )")
        return False
    elif not (value_to_check % 0.25 == 0):
        logger.error(
            f"Error handling hour input {value_to_check}: valid float but invalid graduated"
        )
        return False
    else:
        return True


def purge(storage: store_handler, path):
    if(storage.db_status):
        logger.warning("WARNING: you ask for purging all data - data will be completly lost! Please confirm by typing y, any other character or string will abort: ")
        input_data = input("prees y to continue, anything else to aboort:")
        logger.debug("Input given: {input_data}")
        if (input_data and input_data == len(input_data) * input_data[0] and input_data == "y"):
            logger.info("Purging requested, starting routine deleting db")
            storage.purge(path)
            logger.info("done. Please use --init [hours.minutes] to re-initiate the program")
            sys.exit(0)
        else:
            logger.info("Purge aborted, exiting program")
            sys.exit(0)
    else:
        logger.info("Purging requested, starting routine deleting db")
        storage.purge(path)
        logger.info("done. Please use --init [hours.minutes] to re-initiate the program")
        sys.exit(0)



if __name__ == "__main__":
    main()
