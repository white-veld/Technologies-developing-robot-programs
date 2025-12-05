import random
from datetime import date, timedelta
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Create_tables import Departments, Employees, Suppliers, Products, Orders, OrderItems

fake = Faker()
Faker.seed(42)
random.seed(42)

engine = create_engine("sqlite:///company_data.db")
Session = sessionmaker(bind=engine)
session = Session()

DEPARTMENTS = [
    "IT", "HR", "Sales", "Marketing", "Finance",
    "Logistics", "Operations", "Support", "Development", "Design"
]

CATEGORIES = ["Electronics", "Office", "Network", "Lighting", "Accessories"]

def create_departments():
    objs = [Departments(name=n) for n in DEPARTMENTS]
    session.add_all(objs)
    session.commit()
    return objs


def create_employees(departments, count=120):
    employees = []

    for _ in range(count):
        employees.append(
            Employees(
                full_name=fake.name(),
                position=fake.job(),
                department_id=random.choice(departments).id
            )
        )
    session.add_all(employees)
    session.commit()
    return employees


def create_suppliers(count=40):
    suppliers = []

    for _ in range(count):
        suppliers.append(
            Suppliers(
                company_name=fake.company(),
                contact_email=fake.unique.company_email()
            )
        )
    session.add_all(suppliers)
    session.commit()
    return suppliers


def create_products(suppliers, count=150):
    products = []

    for _ in range(count):
        products.append(
            Products(
                product_name=fake.word().title() + " " + fake.word().title(),
                category=random.choice(CATEGORIES),
                current_stock=random.randint(0, 500),
                min_stock=random.randint(10, 100),
                supplier_id=random.choice(suppliers).id
            )
        )
    session.add_all(products)
    session.commit()
    return products


def create_orders(employees, count=300):
    orders = []
    start = date(2022, 1, 1)
    for _ in range(count):
        orders.append(
            Orders(
                employee_id=random.choice(employees).id,
                order_date=start + timedelta(days=random.randint(0, 900)),
            )
        )
    session.add_all(orders)
    session.commit()
    return orders


def create_order_items(orders, products, count=800):
    items = []
    for _ in range(count):
        prod = random.choice(products)
        items.append(
            OrderItems(
                order_id=random.choice(orders).id,
                product_id=prod.id,
                quantity=random.randint(1, 20),
                price=round(random.uniform(5, 300), 2)
            )
        )
    session.add_all(items)
    session.commit()
    return items


if __name__ == "__main__":
    departments = create_departments()
    employees = create_employees(departments)
    suppliers = create_suppliers()
    products = create_products(suppliers)
    orders = create_orders(employees)
    create_order_items(orders, products)