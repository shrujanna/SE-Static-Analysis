""" INVENTORY SYSTEM: Its an inventory management system to add,
remove,save,load,items with their quanitity """

import json
import logging
from datetime import datetime


def add_item(stock_data, item="default", qty=0, logs=None):
    """
    Adds an item to the stock data and logs the transaction.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to add.
        qty (int): The quantity to add.
        logs (list, optional): The list to append logs to. Defaults to None.
    """
    # Fix for W0102: Dangerous default value
    if logs is None:
        logs = []

    if not item:
        return

    stock_data[item] = stock_data.get(item, 0) + qty

    # Fix for C0209: Use f-string
    log_time = str(datetime.now())
    logs.append(f"{log_time}: Added {qty} of {item}")


def remove_item(stock_data, item, qty):
    """
    Removes a given quantity of an item from the stock data.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to remove.
        qty (int): The quantity to remove.
    """
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        # Catches the specific error and logs as a warning.
        logging.warning("Item '%s' not found, cannot remove.", item)


def get_qty(stock_data, item):
    """
    Gets the quantity of a specific item from stock.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to check.

    Returns:
        int: The quantity of the item, or 0 if not found.
    """
    return stock_data.get(item, 0)  # Use .get for a safe default


def load_data(file="inventory.json"):
    """
    Loads the inventory data from a JSON file.

    Args:
        file (str, optional): The file to load from.

    Returns:
        dict: The loaded inventory data.
    """
    # Fix for R1732 (use 'with') and W1514 (specify encoding)
    try:
        with open(file, "r", encoding="utf-8") as f:
            # Fix for W0603 (global-statement) by returning data instead
            return json.loads(f.read())
    except FileNotFoundError:
        logging.warning("'%s' not found. Starting with empty inventory.", file)
        return {}


def save_data(stock_data, file="inventory.json"):
    """
    Saves the inventory data to a JSON file.

    Args:
        stock_data (dict): The inventory dictionary to save.
        file (str, optional): The file to save to.
    """
    # Fix for R1732 (use 'with') and W1514 (specify encoding)
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(stock_data, indent=4))


def print_data(stock_data):
    """
    Prints a formatted report of all items in stock using logging.

    Args:
        stock_data (dict): The inventory dictionary.
    """
    logging.info("--- Items Report ---")
    for item, quantity in stock_data.items():
        logging.info("%s: %s", item, quantity)
    logging.info("--------------------")


def check_low_items(stock_data, threshold=5):
    """
    Finds all items at or below a given threshold.

    Args:
        stock_data (dict): The inventory dictionary.
        threshold (int, optional): The low-stock threshold. Defaults to 5.

    Returns:
        list: A list of item names that are low in stock.
    """
    result = []
    for item, quantity in stock_data.items():
        if quantity <= threshold:
            result.append(item)
    return result


def main():
    """
    Main function to run the inventory system.
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # stock_data is now a local variable, not global.
    stock_data = load_data()

    # Pass stock_data as an argument to all functions
    add_item(stock_data, "apple", 10)
    add_item(stock_data, "banana", -2)  # This is questionable data

    # This invalid call will now fail clearly
    try:
        add_item(stock_data, 123, "ten")
    except TypeError as e:
        logging.error("Error adding item: %s", e)

    remove_item(stock_data, "apple", 3)
    remove_item(stock_data, "orange", 1)  # This will now log a warning

    logging.info("Apple stock: %s", get_qty(stock_data, 'apple'))
    logging.info("Low items: %s", check_low_items(stock_data))

    save_data(stock_data)
    print_data(stock_data)


if __name__ == "__main__":
    main()
