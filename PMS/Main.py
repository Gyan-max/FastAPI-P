from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Enter ID of the patient', examples = ['P001'])]
    name: Annotated[str, Field(..., description='Enter name of the patient')]
    city: Annotated[str, Field(..., description = 'Enter city of the patient')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Enter age of the patient')]
    gender: Annotated[str, Field(..., description='Enter gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Enter height of the patient in meters')]
    weight: Annotated[float, Field(..., gt=0, description='Enter weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Under-Weight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'
        
class update_Patient_Details(BaseModel):
    name: Annotated[str | None, Field(default=None, description='Enter name of the patient')]
    city: Annotated[str | None, Field(default=None, description='Enter city of the patient')]
    age: Annotated[int | None, Field(default=None, gt=0, lt=120, description='Enter age of the patient')]
    gender: Annotated[str | None, Field(default=None, description='Enter gender of the patient')]
    height: Annotated[float | None, Field(default=None, gt=0, description='Enter height of the patient in meters')]
    weight: Annotated[float | None, Field(default=None, gt=0, description='Enter weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float | None:
        if self.weight is not None and self.height is not None:
            return round(self.weight/self.height**2, 2)
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
        with open('patients.json', 'r') as f:
            data = json.load(f)
        return data

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
        if patient.city is not None:
            data[patient_id]['city'] = patient.city
        if patient.age is not None:
            data[patient_id]['age'] = patient.age
        if patient.gender is not None:
            data[patient_id]['gender'] = patient.gender
        if patient.height is not None:
            data[patient_id]['height'] = patient.height
        if patient.weight is not None:
            data[patient_id]['weight'] = patient.weight
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