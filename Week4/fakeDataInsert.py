import random
from faker import Faker
import datetime

fake = Faker()
positions = [
    'Software Engineer', 'Data Analyst', 'DevOps Engineer', 'ML Engineer', 'QA Engineer',
    'Backend Developer', 'Frontend Developer', 'Cloud Architect', 'SysAdmin', 'Data Scientist'
]

start = datetime.date(2015, 1, 1)
end = datetime.date(2024, 6, 1)

for i in range(50):
    name = fake.name().replace("'", "''")  # Escape single quotes
    position = random.choice(positions)
    start_date = fake.date_between(start_date=start, end_date=end)
    salary = random.randint(60000, 200000)
    print(f"INSERT INTO employees (name, position, start_date, salary) VALUES('{name}', '{position}', '{start_date}', {salary});")