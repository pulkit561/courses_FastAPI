import sys
sys.path.append("./src/")
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from routes.course_endpoints import course_router
from routes.chapter_endpoints import chapter_router
import uvicorn


app = FastAPI()

@app.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": form_data.username, "token_type": "bearer"}

app.include_router(course_router, prefix="/courses")
app.include_router(chapter_router, prefix="/chapters")

if __name__ == "__main__":
    uvicorn.run("main:app", host = "localhost", port = 8000, reload=True)