from typing import Annotated, Optional
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from model.course import Course
from motor import motor_asyncio
from config import MONGODB_HOST, MONGODB_PORT

course_router = APIRouter()
client = motor_asyncio.AsyncIOMotorClient(f'mongodb://{MONGODB_HOST}:{MONGODB_PORT}')
db = client['course_database']
courses_collection = db.get_collection('Course')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class CourseEndpoint:

    def __init__(self) -> None:
        pass

    @course_router.get("/getallcourses/sort/{sort}")
    async def get_all_courses(token: Annotated[str, Depends(oauth2_scheme)], sort: str, domain: Optional[str] = None):
        sort_key = "name" if sort == "alphabetical" else "date" if sort == "date" else "courseRating" if sort == "total course rating" else "invalid"
        if sort_key == "invalid":
            raise HTTPException(status_code=400, detail="Invalid sort mode")
        sort_value = 1 if sort =="alphabetical" else -1

        # Building aggregate pipeline to perform join on domains collection
        pipeline = []
        if domain:
            pipeline.append({
                "$lookup": {
                    "from": "Domain",
                    "localField": "domain",
                    "foreignField": "_id",
                    "as": "domains"
                }
            })
            pipeline.append({
                "$match": {
                    "domains.name": domain
                }
            })
        
        pipeline.append({
            "$sort": {
                sort_key: sort_value
            }
        })

        courses_data = await courses_collection.aggregate(pipeline).to_list(length=None)
        if courses_data:
            courses = [Course.parse_obj(course_data) for course_data in courses_data]
            return courses

        raise HTTPException(status_code=404, detail="No courses found")

    @course_router.get("/getcourseoverview/{course_id}")
    async def get_course_overview(token: Annotated[str, Depends(oauth2_scheme)], course_id: str):
        course_data = await courses_collection.find_one({"_id": course_id})
        if not course_data:
            raise HTTPException(status_code=404, detail=f"Course with id = {course_id} not found")

        # Parsing using pydantic BaseModel
        course_description = Course.parse_obj(course_data).description
        return course_description
    







