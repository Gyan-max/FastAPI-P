from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Enter ID of the patient', examples = ['P001'])]


    name: Annotated[str, Field(..., description='Enter name of the patient')]
    father_name: Annotated[str, Field(..., description='Enter name of the father of the patient')]
    mother_name: Annotated[str, Field(..., description='Enter name of the mother of the patient')]
    grandfather_name: Annotated[str, Field(..., description='Enter name of the grandfather of the patient')]
    grandmother_name: Annotated[str, Field(..., description='Enter name of the grandmother of the patient')]
    phone: Annotated[str, Field(..., description='Enter phone number of the patient', examples = ['1234567890'])]

    address: Annotated[str, Field(..., description = 'Enter city of the patient')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Enter age of the patient')]
    gender: Annotated[str, Field(..., description='Enter gender of the patient')]
    bp: Annotated[float, Field(..., gt=0, description='Enter blood pressure of the patient in mmHg')]
    sugar: Annotated[float, Field(..., gt=0, description='Enter sugar level of the patient in mg/dL')]
    temperature: Annotated[float, Field(..., gt=0, description='Enter temperature of the patient in Celsius')]
    reason: Annotated[str, Field(..., description='Enter reason for visit of the patient')]


    # @computed_field
    # @property
    # def bmi(self) -> float:
    #     bmi = round(self.sugar/(self.bp**2), 2)
    #     return bmi
    
    # @computed_field
    # @property
    # def verdict(self) -> str:
    #     if self.bmi < 18.5:
    #         return 'Under-Weight'
    #     elif self.bmi < 25:
    #         return 'Normal'
    #     elif self.bmi < 30:
    #         return 'Over-Weight'
    #     else:
    #         return 'Obese'
    #     elif self.bmi < 30:
    #         return 'Normal'
    #     else:
    #         return 'Obese'
        
class update_Patient_Details(BaseModel):
    name: Annotated[str | None, Field(default=None, description='Enter name of the patient')]
    father_name: Annotated[str | None, Field(default=None, description='Enter name of the father of the patient')]
    mother_name: Annotated[str | None, Field(default=None, description='Enter name of the mother of the patient')]
    grandfather_name: Annotated[str | None, Field(default=None, description='Enter name of the grandfather of the patient')]
    grandmother_name: Annotated[str | None, Field(default=None, description='Enter name of the grandmother of the patient')]
    phone: Annotated[str | None, Field(default=None, description='Enter phone number of the patient', examples = ['1234567890'])]
    address: Annotated[str | None, Field(default=None, description='Enter city of the patient')]
    age: Annotated[int | None, Field(default=None, gt=0, lt=120, description='Enter age of the patient')]
    gender: Annotated[str | None, Field(default=None, description='Enter gender of the patient')]
    bp: Annotated[float | None, Field(default=None, gt=0, description='Enter blood pressure of the patient in mmHg')]
    sugar: Annotated[float | None, Field(default=None, gt=0, description='Enter sugar level of the patient in mg/dL')]
    temperature: Annotated[float | None, Field(default=None, gt=0, description='Enter temperature of the patient in Celsius')]
    reason: Annotated[str | None, Field(default=None, description='Enter reason for visit of the patient')]

    @computed_field
    @property
    def bmi(self) -> float | None:
        if self.weight is not None and self.bp is not None:
            return round(self.weight/self.bp**2, 2)
        else:
            return None
        
    @computed_field
    @property
    def verdict(self) -> str | None:
        if self.bmi is not None:
            if self.bmi < 18.5:
                return 'Under-Weight'
            elif self.bmi < 25:
                return 'Normal'
            elif self.bmi < 30:
                return 'Over-Weight'
            else:
                return 'Obese'
        else:
            return None
def patient_details():
    try:
        with open('patients.json', 'r') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Invalid JSON structure")
            return data
    except (json.JSONDecodeError, ValueError):
        return {}  # Return an empty dictionary if the file is invalid or empty
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)
    

    
@app.get('/')
def root():
    return 'Welcome to Patient Management System API'    

@app.get('/about')
def about():
    return 'This API provides a comprehensive Patient Management System.'

@app.get('/view')
def view():
    return patient_details()

@app.get('/patients/{patient_id}')
def get_patient_details(patient_id: str = Path(..., description='Enter ID of the patient')):
    data = patient_details()
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail = 'Patient not found in database')
    
@app.post('/create')
def create_patient(patient: Patient):
    data = patient_details()
    if patient.id in data:
        raise HTTPException(status_code=400, detail = 'Patient already exists in the database')
    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)
    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient: update_Patient_Details):
    data = patient_details()
    if patient_id in data:
        if patient.name is not None:
            data[patient_id]['name'] = patient.name
        if patient.father_name is not None:
            data[patient_id]['father_name'] = patient.father_name
        if patient.mother_name is not None:
            data[patient_id]['mother_name'] = patient.mother_name
        if patient.grandfather_name is not None:
            data[patient_id]['grandfather_name'] = patient.grandfather_name
        if patient.grandmother_name is not None:
            data[patient_id]['grandmother_name'] = patient.grandmother_name
        if patient.phone is not None:
            data[patient_id]['phone'] = patient.phone
        if patient.address is not None:
            data[patient_id]['address'] = patient.address
        if patient.age is not None:
            data[patient_id]['age'] = patient.age
        if patient.gender is not None:
            data[patient_id]['gender'] = patient.gender
        if patient.bp is not None:
            data[patient_id]['bp'] = patient.bp
        if patient.sugar is not None:
            data[patient_id]['sugar'] = patient.sugar
        if patient.temperature is not None:
            data[patient_id]['temperature'] = patient.temperature
        if patient.reason is not None:
            data[patient_id]['reason'] = patient.reason
        save_data(data)
        return JSONResponse(status_code=200, content={'message': 'Patient updated successfully'})
    else:
        raise HTTPException(status_code=404, detail = 'Patient not found in the database')

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = patient_details()
    if patient_id in data:
        del data[patient_id]
        save_data(data)
        return JSONResponse(status_code=200, content={'message': 'Patient deleted successfully'})
    else:
        raise HTTPException(status_code=404, detail = 'Patient not found in the database')