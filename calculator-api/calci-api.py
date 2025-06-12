from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from enum import Enum


app = FastAPI()

class ClaculatorInput(BaseModel):
    num1: int | float 
    num2: int | float
    # input_type: str = Field(..., description="Type of operation: add, subtract, multiply, divide")

    class operatorType(str, Enum):
        add = "+"
        subtract = "-"
        multiply = "*"
        divide = "/"
    operation: operatorType = Field(..., description="Operation to perform")

    @computed_field
    @property
    def addition(self) -> int | float:
        if isinstance(self.num1, (int, float)) and isinstance(self.num2, (int, float)):
            return self.num1 + self.num2
        else:
            return "Invalid input for addition"
        
    @computed_field
    @property
    def substraction(self) -> int | float:
        if isinstance(self.num1, (int, float)) and isinstance(self.num2, (int, float)):
            return self.num1 - self.num2
        else:
            return "Invalid input for subtraction"
    
    @computed_field
    @property
    def multiplication(self) -> int | float:
        if isinstance(self.num1, (int, float)) and isinstance(self.num2, (int, float)):
            return self.num1 * self.num2
        else:
            return "Invalid input for multiplication"
    @computed_field
    @property
    def division(self) -> int | float:
        if isinstance(self.num1, (int, float)) and isinstance(self.num2, (int, float)):
            if self.num2 != 0:
                return self.num1 / self.num2
            else:
                return "Division by zero is not allowed"
        else:
            return "Invalid input for division"

@app.post("/calculate")
def calculate(input_data: ClaculatorInput):
    if input_data.operation == ClaculatorInput.operatorType.add:
        return {"result": input_data.addition}
    elif input_data.operation == ClaculatorInput.operatorType.subtract:
        return {"result": input_data.substraction}
    elif input_data.operation == ClaculatorInput.operatorType.multiply:
        return {"result": input_data.multiplication}
    elif input_data.operation == ClaculatorInput.operatorType.divide:
        return {"result": input_data.division}
    else:
        return {"error": "Invalid input type. Use add, subtract, multiply, or divide."}
@app.get("/")
def read_root():
    return {"message": "Welcome to the Calculator API! Use POST /calculate with num1, num2, and input_type to perform calculations."}

@app.get("/about")
def about():
    return {
        "name": "Calculator API",
        "version": "1.0.0",
        "description": "A simple API to perform basic arithmetic operations like addition, subtraction, multiplication, and division."
    }
