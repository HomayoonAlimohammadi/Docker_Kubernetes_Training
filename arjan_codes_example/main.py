from dataclasses import dataclass, field
import json
from typing import Dict, List
from fastapi import FastAPI, HTTPException, Response


app = FastAPI()


@dataclass
class Employee:
    id: str
    name: str
    tags: List[str] = field(default_factory=list)
    description: str = ""


def read_data(path_to_data: str) -> Dict[str, Employee]:
    employees: Dict[str, Employee] = {}
    with open(path_to_data, "r") as f:
        data = json.load(f)
        for employee_data in data:
            employee = Employee(**employee_data)
            employees[employee.id] = employee
    return employees


@app.get("/")
def index_view() -> Response:
    return Response("The API is up and running! Yeay!")


@app.get("/employees/")
def get_employee_list() -> Dict[str, Employee]:
    return employees


@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee_details(employee_id: str) -> Employee:
    if employee_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found!")
    return employees[employee_id]


employees = read_data("./employees_data.json")
