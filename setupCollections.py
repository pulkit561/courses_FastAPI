import json
from pymongo import MongoClient, ASCENDING, DESCENDING
from uuid import uuid4

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

class SetupCollections:
    
    def __init__(self) -> None:
        print("MongoDB collections setup started ...")

        self.client = MongoClient(f'mongodb://{MONGODB_HOST}:{MONGODB_PORT}/')
        self.db = self.client['course_database']
        self.courses_collection = self.db['Course']
        self.domains_collection = self.db['Domain']
        self.chapters_collection = self.db['Chapter']

        print("Reading courses.json ...")
        with open('./courses.json') as file:
            courses_data = json.load(file)

        for course in courses_data:
            # Extract course data
            course_name = course['name']
            course_date = course['date']
            course_description = course['description']
            course_domains = course['domain']
            course_chapters = course['chapters']

            course_domain_ids = []
            course_chapter_ids = []

            print(f"Inserting data into Domain collection for course : {course_name} ...")
            # Insert domain into Domain collection if it doesn't exist
            for domain in course_domains:
                domain_id = ""
                if not self.domains_collection.find_one({'name': domain}):
                    domain_id = uuid4().hex
                    self.domains_collection.insert_one({
                        '_id': domain_id,
                        'name': domain
                    })
                else:
                    domain_id = self.domains_collection.find_one({'name': domain})['_id']
                course_domain_ids.append(domain_id)

            print(f"Inserting data into Chapter collection for course : {course_name} ...")
            # Insert chapters into Chapter collection
            for chapter in course_chapters:
                chapter_name = chapter['name']
                chapter_text = chapter['text']
                chapter_id = uuid4().hex
                self.chapters_collection.insert_one({
                    '_id': chapter_id,
                    'name': chapter_name,
                    'text': chapter_text,
                    'rating': 0
                })
                course_chapter_ids.append(chapter_id)

            print(f"Inserting data into Course collection for course : {course_name} ...")
            # Insert course into Course collection
            self.courses_collection.insert_one({
                '_id': uuid4().hex,
                'name': course_name,
                'date': course_date,
                'description': course_description,
                'domain': course_domain_ids,
                'chapters': course_chapter_ids,
                'courseRating': 0
            })

        print("Creating appropriate indexes ...")
        self.courses_collection.create_index([('name', ASCENDING), ('date', DESCENDING), ('courseRating', DESCENDING)])

        print("MongoDB collections are setup with data")

if __name__ == "__main__":
    SetupCollections()







