import csv
import traceback
import os 
import custom_module





#--------------------------------2


def read_employees():
    try:

        employees_dict = {}
        rows_list = []

    
        with open("../csv/employees.csv", "r", newline ="", encoding = "utf -8") as csvfile:
            reader = csv.reader(csvfile)

            employees_dict['fields'] = next(reader)
            for row in reader:
                rows_list.append(row)

            employees_dict['rows'] = rows_list

        return employees_dict  
    

    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File: {trace[0]}, Line: {trace[1]}, Function: {trace[2]}, Message: {trace[3]}')
        
        print(f"An exception occurred.")
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")
        exit(1) 

employees = read_employees()
print(employees)



#--------------------------------3



def column_index(column_name):
    return employees["fields"].index(column_name)

employee_id_column = column_index("employee_id")



#--------------------------------4

#def column_index(column_name):
def first_name(row_number):
     first_name_col_index = column_index("first_name")
     employee_row = employees["rows"][row_number]
     return employee_row[first_name_col_index]


#--------------------------------5   

def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    matches = list(filter(employee_match, employees["rows"]))
    return matches

#--------------------------------6
def employee_find_2(employee_id):
    matches = list(filter(lambda row: int(row[employee_id_column]) == employee_id, employees["rows"]))
    return matches

#--------------------------------7

def sort_by_last_name():
    last_name_column = column_index("last_name")

    employees['rows'].sort(key = lambda row: row[last_name_column])
    return employees["rows"]

#--------------------------------8

def employee_dict(row):
    return {
        field: row[i]
        for i, field in enumerate(employees["fields"])
        if field != "employee_id"
            
    }       


#--------------------------------9

def all_employees_dict():
    return {
        row[employees["fields"].index("employee_id")]: employee_dict(row)
        for row in employees["rows"]
    }

#--------------------------------10

def get_this_value():
    return os.getenv("THISVALUE")

#--------------------------------11

def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)

set_that_secret("open_sesame")


#--------------------------------12


def read_csv_to_dict(filepath):
     with open('./minutes.csv', newline = '', encoding= 'utf-8') as csvfile:
         reader = csv.reader(csvfile)
         fields = next (reader)
         rows = [tuple(row) for row in reader]
     return {"fields": fields, "rows": rows}    

def read_minutes():
    minutes1 = read_csv_to_dict("./minutes.csv")
    minutes2 = read_csv_to_dict("./minutes.csv")
    return minutes1, minutes2

minutes1, minutes2 = read_minutes()


#--------------------------------13

def create_minutes_set():
    set1 = set(minutes1["rows"])
    set2 = set(minutes1["rows"])
    return set1.union(set2)

minutes_set = create_minutes_set()
