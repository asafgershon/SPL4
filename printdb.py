from persistence import *

def print_table(table_name, order_by):
    """Fetch and print a table sorted by a given column."""
    cursor = repo._conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} ORDER BY {order_by}")
    rows = cursor.fetchall()

    print(table_name)  # print table name
    for row in rows:
        print(row)  # print each row

def print_employees_report():
    """Print detailed employee report: Name, Salary, Location, Total Sales Income"""
    print("Employees report")

    cursor = repo._conn.cursor()
    cursor.execute("""
        SELECT employees.name, employees.salary, branches.location,
               COALESCE(SUM(products.price * abs(activities.quantity)), 0) AS total_sales_income
        FROM employees
        JOIN branches ON employees.branche = branches.id
        LEFT JOIN activities ON employees.id = activities.activator_id AND activities.quantity < 0
        LEFT JOIN products ON activities.product_id = products.id
        GROUP BY employees.id
        ORDER BY employees.name
    """)

    rows = cursor.fetchall()
    for row in rows:
        print(row)  # print as tuple

def print_activity_report():
    """Print detailed activity report: Date, Item Description, Quantity, Seller Name, Supplier Name"""
    cursor = repo._conn.cursor()
    cursor.execute("""
        SELECT activities.date, products.description, activities.quantity,
               CASE WHEN activities.quantity < 0 THEN employees.name ELSE 'None' END AS seller_name,
               CASE WHEN activities.quantity > 0 THEN suppliers.name ELSE 'None' END AS supplier_name
        FROM activities
        JOIN products ON activities.product_id = products.id
        LEFT JOIN employees ON activities.activator_id = employees.id AND activities.quantity < 0
        LEFT JOIN suppliers ON activities.activator_id = suppliers.id AND activities.quantity > 0
        ORDER BY activities.date
    """)

    rows = cursor.fetchall()

    if rows:
        print("Activities report")
        for row in rows:
            print(row)  # print as tuple

def main():
    """Print all tables and reports in the required order."""
    print_table("activities", "date")
    print_table("branches", "id")
    print_table("employees", "id")
    print_table("products", "id")
    print_table("suppliers", "id")
    print_employees_report()
    print_activity_report()

if __name__ == '__main__':
    main()
