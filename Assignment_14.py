"""
Experiment 14: Logging module
Record messages of different severity levels (DEBUG, INFO, WARNING, ERROR,
CRITICAL) to both the console and a file.
"""

import logging
import os

LOG_FILE = "app.log"
LEVELS = {
    "1": ("DEBUG", logging.DEBUG),
    "2": ("INFO", logging.INFO),
    "3": ("WARNING", logging.WARNING),
    "4": ("ERROR", logging.ERROR),
    "5": ("CRITICAL", logging.CRITICAL),
}


def setup_logger():
    """Configure logger with a console handler and a file handler."""
    logger = logging.getLogger("MyApp")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")

    # Set level for handlers
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)

    # Create formatters and add them to handlers
    console_format = logging.Formatter("%(levelname)s - %(message)s")
    file_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                                    datefmt="%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger, console_handler


def log_all_levels(logger):
    logger.debug("This is a DEBUG message (detailed info for developers)")
    logger.info("This is an INFO message (general program flow)")
    logger.warning("This is a WARNING message (something to look into)")
    logger.error("This is an ERROR message (an unexpected problem)")
    logger.critical("This is a CRITICAL message (serious error)")


def log_custom(logger):
    print("Levels: 1.DEBUG  2.INFO  3.WARNING  4.ERROR  5.CRITICAL")
    level = LEVELS.get(input("Choose level (1-5): ").strip())
    if not level:
        print("Invalid level.")
        return
    message = input("Enter your message: ").strip()
    logger.log(level[1], message)


def change_console_level(console_handler):
    #Om Kutwal Sy-12 Roll no. 70
    print("Levels: 1.DEBUG  2.INFO  3.WARNING  4.ERROR  5.CRITICAL")
    level = LEVELS.get(input("Choose new console level (1-5): ").strip())
    if not level:
        print("Invalid level.")
        return
    console_handler.setLevel(level[1])
    print(f"Console now shows {level[0]} and above. (File still records everything.)")


def log_exception(logger):
    donuts, guests = 5, 0
    try:
        donuts / guests
    except ZeroDivisionError:
        logger.exception("DonutCalculationError")


def log_variable(logger):
    name = input("Enter a value to log: ").strip()
    logger.debug("name=%s", name)
    logger.info("User entered: %s", name)


def show_file():
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        print(f"'{LOG_FILE}' is empty or not created yet.")
        return
    print(f"\n--- Content of {LOG_FILE} ---")
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        print(f.read())


def clear_file(logger):
    for h in logger.handlers:
        if isinstance(h, logging.FileHandler):
            h.close()
    open(LOG_FILE, "w").close()
    print(f"'{LOG_FILE}' cleared.")


def print_menu():
    print("\n===== LOGGING PROGRAM =====")
    print("1. Log messages of all levels")
    print("2. Log a custom message at a chosen level")
    print("3. Change console log level")
    print("4. Log an exception with stack trace")
    print("5. Log a variable value")
    print("6. Display log file")
    print("7. Clear log file")
    print("8. Exit")
    print("===========================")


def main():
    logger, console_handler = setup_logger()
    while True:
        print_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            log_all_levels(logger)
        elif choice == "2":
            log_custom(logger)
        elif choice == "3":
            change_console_level(console_handler)
        elif choice == "4":
            log_exception(logger)
        elif choice == "5":
            log_variable(logger)
        elif choice == "6":
            show_file()
        elif choice == "7":
            clear_file(logger)
            logger, console_handler = setup_logger()
        elif choice == "8":
            print("Exiting the Logging Program. Goodbye!")
            logging.shutdown()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
