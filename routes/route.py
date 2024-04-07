from fastapi import APIRouter, HTTPException, Query, Path,Response
from config.database import db
from models.students import Student
from models.students import CreateStudentResponse
from models.students import StudentResponse
from models.students import ListStudentsResponse
from bson import ObjectId


router = APIRouter()

students_collection = db.students



#create student data
@router.post("/students", status_code=201, response_model=CreateStudentResponse, response_description="A JSON response sending back the ID of the newly created student record.")
async def create_student(student: Student, response: Response):
    """
    API to create a student in the system. All fields are mandatory and required while creating the student in the system.
    """
    # Insert student into MongoDB
    result = students_collection.insert_one(student.dict())
    
    # Return the ID of the newly created student
    response.headers["Content-Type"] = "application/json"
    return {"id": str(result.inserted_id)}




#list the student data
@router.get("/students", response_model=ListStudentsResponse)
async def list_students(
    country: str = Query(None, description="To apply filter of country. If not given or empty, this filter should be applied."),
    age: int = Query(None, description="Only records which have age greater than or equal to the provided age should be present in the result. If not given or empty, this filter should be applied.")
):
    """
    An API to find a list of students. You can apply filters on this API by passing the query parameters as listed below.
    """
    # Prepare filter for MongoDB query
    filter_query = {}
    if country:
        filter_query["address.country"] = country
    if age is not None:
        filter_query["age"] = {"$gte": age}

    # Retrieve students from MongoDB based on the filter
    students = list(students_collection.find(filter_query, {"_id": 0}))

    # Return the list of students
    return {"data": students}



#get one student data
@router.get("/students/{id}", response_model=Student,summary="Fetch Student")
async def get_student(id: str = Path(..., description="The ID of the student previously created.")):
    object_id = ObjectId(id)
    # Retrieve student from MongoDB
    student = students_collection.find_one({"_id":object_id}, {"_id": 0})

    # Check if student exists
    if student:
        return student
    else:
        # If student not found, raise HTTPException with status code 404
        raise HTTPException(status_code=404, detail="Student not found")


#update student data
@router.patch("/students/{id}", status_code=204,response_description="No content")
async def update_student(student: Student, id: str = Path(..., description="The ID of the student previously created.")):
    """
    API to update the student's properties based on information provided. Not mandatory that all information would be sent in PATCH, only what fields are sent should be updated in the Database.
    """
    # Prepare update data
    update_data = student.dict(exclude_unset=True)

    # Update student in MongoDB
    result = students_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})

    # Check if student exists
    if result.modified_count == 0:
        # If student not found, raise HTTPException with status code 404
        raise HTTPException(status_code=404, detail="Student not found")

    # Return an empty dictionary as the response body
    return {}

#delete data
@router.delete("/students/{id}")
async def delete_student(id: str = Path(..., description="The ID of the student to delete.")):
    
    # Delete student from MongoDB
    result = students_collection.delete_one({"_id": ObjectId(id)})

    # Check if student exists
    if result.deleted_count == 0:
        # If student not found, raise HTTPException with status code 404
        raise HTTPException(status_code=404, detail="Student not found")
