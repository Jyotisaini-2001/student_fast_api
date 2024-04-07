from pydantic import BaseModel
from typing import List


class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address
class CreateStudentResponse(BaseModel):
    id: str
class StudentResponse(BaseModel):
    name: str
    age: int
class ListStudentsResponse(BaseModel):
    data: List[StudentResponse]