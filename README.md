# courses_FastAPI
Containerized python app with FastAPI endpoints using MongoDB

# Dependencies
 - Included in **requirements.txt**
 - Besides packages, **pip** and **docker** are needed

# Steps to run
  1. Setup MongoDB collections with **setupCollections.py**.  
  1. Go to the folder containing Dockerfile.  
  2. `docker build -t {docker-image} .`
  3. `docker run -p 8000:8000 {docker-image}`
  4. If you want to run the app locally use **MONGODB_HOST = 'localhost'** in src/config.py. By default **MONGODB_HOST**      is configured to access the host machine from within the container. 
  5. To run **tests** on localhost please follow step 5 then go to **src/tests** and run `pytest`

# Comments
## Script for setting up mongoDB database
 - Used **pymongo** to setup 3 collections - **Course**, **Chapter**, **Domain** by parsing the given courses.json.  
 - Course collection contains foreign keys **uuid4()** strings to refer to Domain and Chapter. This was done for better    maintainability and evolvability of data.  

## Containerized app
 - Used **pydantic BaseModel** to represent each entity: Course, Chapter and Domain. Present inside src/model.
 - Endpoints are exposed in src/routes. Also added **OAuth2** protection for APIs.  
 - Used **motor** to make APIs asynchronous as the problem stated the APIs will directly serve a front-end                  application.
 - Raised **HTTPExceptions** inside APIs where required.  
 - Used **aggregator** framework to serve GET courses in sorted order as it involved looking up Domain collection. 
  
**Bonus**: Added *OAuth2* to make APIs secure from unauthorized users. Did not store user information with hashed credentials in the database but it can be an extension for business use case.
 
 ## Tests
  - Used **FastAPI TestClient** and **pytest** to write tests for all endpoints.  
  - Please refer to files inside src/tests/. If the data corresponding to IDs used for tests is changed, they might         fail. 


