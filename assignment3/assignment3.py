import pandas as pd
import json
import numpy as np


#----------task1

data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

task1_data_frame = pd.DataFrame(data)
print(task1_data_frame)

task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000] 

print(task1_with_salary)

task1_older = task1_with_salary.copy()

task1_older['Age'] += 1
print(task1_older)
task1_older.to_csv('employees.csv', index=False)

#----------task2

task2_employees = pd.read_csv('employees.csv')
print(task2_employees)

additional_employees = [
    {"Name": "Eve", "Age": 28, "City": "Miami", "Salary": 60000},
    {"Name": "Frank", "Age": 40, "City": "Seattle", "Salary": 95000}
]

with open('additional_employees.json', 'w') as json_file:
    json.dump(additional_employees, json_file)

json_employees = pd.read_json('additional_employees.json')

print(json_employees)

more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)
print(more_employees)

#----------task3 
first_three = more_employees.head(3)
print(first_three)

last_two = more_employees.tail(2)
print(last_two)

employee_shape = more_employees.shape
print(employee_shape)
more_employees.info()

#----------task4

dirty_data = pd.read_csv('dirty_data.csv')
print(dirty_data)
clean_data = dirty_data.copy()
clean_data = clean_data.drop_duplicates()
print(clean_data)

clean_data['Age'] = pd.to_numeric(clean_data['Age'], errors='coerce')
print(clean_data)

clean_data['Salary'] = pd.to_numeric(clean_data['Salary'].replace(['unknown', 'n/a'], np.nan), errors='coerce')
print(clean_data)

clean_data['Age'] = clean_data['Age'].fillna(clean_data['Age'].mean())
clean_data['Salary'] = clean_data['Salary'].fillna(clean_data['Salary'].median())
print(clean_data)

clean_data['Hire Date'] = pd.to_datetime(clean_data['Hire Date'], errors='coerce')
print(clean_data)

clean_data['Name'] = clean_data['Name'].str.strip().str.upper()
clean_data['Department'] = clean_data['Department'].str.strip().str.upper()
print(clean_data)

