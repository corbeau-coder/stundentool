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
        "time_value",
        type=float,
        help="time to scraped of the overhang budget. Schema HOURS.MINUTES - only 4 values are allowed for minutes: 00,25,50,75 reflecting that we usually round costs in 15 minute graduation",
        nargs='?'
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
    parser.add_argument("--verbose", action="store_true")
    

    args = parser.parse_args()
    

    if args.verbose:
        logger.level("DEBUG")
        logger.info("Verbose logging configured")
    else:
        logger.level("INFO")
        logger.info("Normal logging configured")

    logger.debug("Loading DB and checking state...")
    storage = store_handler(path)
    logger.debug(f" DB check returns {storage.db_status}. done")



    routing_value = args.purge << 3 | args.init << 2 | args.add << 1 | args.status
    logger.debug(f"Routing value is {routing_value}")
    match routing_value:
        case 1:
            printout(storage, args.verbose)         
            sys.exit(0)
        case 2:
            if args.time_value is not None:
                if (graduation_checker(args.time_value)):
                    new_data = data_object(args.time_value)
                    storage.write_one(new_data)
                    sys.exit(0)
                else:
                    sys.exit(1)
            else:
                logger.error("Error: empty hours.minutes argument, cannot add entry.")
                sys.exit(1)
        case 4:
            if args.time_value is not None:
                if (graduation_checker(args.time_value)):
                    storage.init(args.time_value)
                    #RETURN falsch, es wird nicht richtig auf exceptions reagiert
                    sys.exit(0)
                else:
                    sys.exit(1)

            storage.init(args.time_value)
        case 8:
            purge(storage, path)
        case _:
            logger.error("Error: check parameter set used - do not combine purge, init, status or add as parameters")
            sys.exit(1)

        
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
        logger.debug(f"Input given: {input_data}")
        if (input_data and input_data == len(input_data) * input_data[0] and input_data == "y"):
            logger.info("Purging requested, starting routine deleting db")
            ret, e_str = storage.purge(path)
            if not ret:
                logger.warning(f"warning: during db removal error occured: {e_str}")
            logger.info("done. Please use --init [hours.minutes] to re-initiate the program")
            sys.exit(0)
        else:
            logger.info("Purge aborted, exiting program")
            sys.exit(0)
    else:
        logger.info("Purging requested, starting routine deleting db")
        ret, e_str = storage.purge(path)
        if not ret:
            logger.warning(f"warning: during db removal error occured: {e_str}")
        logger.info("done. Please use --init [hours.minutes] to re-initiate the program")
        sys.exit(0)


def printout(storage: store_handler, verbose: bool) -> None:
    if (verbose):
        #TODO: Verbose output including stats
        logger.info("TODO")
    else:
        initial, reduced = storage.calc(storage.read_all())
        logger.info(f"hours initial: {initial}\nhours reduced already: {reduced}\n\nhours left: {initial - reduced}\n\nuse --verbose parameter additionally for more stats")
    return



if __name__ == "__main__":
    main()
