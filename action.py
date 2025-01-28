from persistence import *

import sys


def process_action(action_line):
    # splitting the action line into separate values
    product_id = int(action_line[0])
    quantity = int(action_line[1])
    activator_id = int(action_line[2])
    date = action_line[3] #keep the date string

    # checking if the product exists in the database
    cursor = repo._conn.cursor()  # creating a cursor to interact with the database
    cursor.execute("SELECT quantity FROM products WHERE id=?", (product_id,))  # query to get product quantity
    product = cursor.fetchone()  # fetching the result

    if product is None:
        return  # if the product does not exist, do nothing and exit function

    current_quantity = product[0]  # extracting current quantity from the result

    if quantity < 0 and abs(quantity) > current_quantity:
        return  # if trying to sell more than available, do nothing and exit function

    # updating the product quantity in the database
    new_quantity = current_quantity + quantity  # calculating new quantity
    cursor.execute("UPDATE products SET quantity=? WHERE id=?", (new_quantity, product_id))  # update query

    # inserting the action into the activities table
    cursor.execute(
        "INSERT INTO activities (product_id, quantity, activator_id, date) VALUES (?, ?, ?, ?)",
        (product_id, quantity, activator_id, date),
    )

    repo._conn.commit()  # saving changes to the database

def main(args : list[str]):
    inputfilename : str = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(", ")
            process_action(splittedline)

if __name__ == '__main__':
    main(sys.argv)