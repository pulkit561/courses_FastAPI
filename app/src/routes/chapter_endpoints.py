from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from model.chapter import Chapter
from motor import motor_asyncio
from config import MONGODB_HOST, MONGODB_PORT
from typing import Annotated

chapter_router = APIRouter()
client = motor_asyncio.AsyncIOMotorClient(f'mongodb://{MONGODB_HOST}:{MONGODB_PORT}')
db = client['course_database']
chapters_collection = db.get_collection('Chapter')
courses_collection = db.get_collection('Course')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class ChapterEndpoints:

    def __init__(self) -> None:
        pass

    @chapter_router.get("/getchapter/{chapter_id}")
    async def get_chapter(token: Annotated[str, Depends(oauth2_scheme)], chapter_id: str):
        chapter_data = await chapters_collection.find_one({"_id": chapter_id})
        if not chapter_data:
            raise HTTPException(status_code=404, detail=f"chapter with id = {chapter_id} not found")

        chapter = Chapter.parse_obj(chapter_data)
        return chapter
        

    @chapter_router.post("/ratechapter/{chapter_id}/rating/{rating}", status_code=200)
    async def rate_chapter(token: Annotated[str, Depends(oauth2_scheme)], chapter_id: str, rating: int):
        chapter_data = await chapters_collection.find_one({"_id": chapter_id})
        if not chapter_data:
            raise HTTPException(status_code=404, detail=f"chapter with id = {chapter_id} not found")

        # For finding the course containing this chapter
        course_data = await courses_collection.find_one({"chapters": {"$in": [chapter_id]}})
        if not course_data:
            raise HTTPException(status_code=404, detail=f"No course contains chapter with id = {chapter_id}")

        course_id = course_data['_id']

        # Update chapter rating
        await chapters_collection.update_one({"_id": chapter_id}, {"$set": {"rating": rating}})
        # Update course rating
        await courses_collection.update_one({"_id": course_id}, {"$inc": {"courseRating": rating}})


