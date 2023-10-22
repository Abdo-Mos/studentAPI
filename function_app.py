import azure.functions as func
import logging
import json

import pymongo

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

#  initializing DB
try: 
    db_client = pymongo.MongoClient("mongodb://localhost:27017")
    db = db_client["main_db"]
    db_collection = db["student"]
except:
    print("Error connecting to DB")

func.HttpResponse.mimetype = 'application/json'
func.HttpResponse.charset = 'utf-8'


'''
Ref code: return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
'''
@app.route(route="studentAPI")
def studentAPI(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # handling the GET method
    if req.method == 'GET':
        # getting the id as a param from URL
        id = req.params.get('id')
        # get the student with the id from the db collection
        student = db_collection.find_one({'id': int(id)})
        # clean the db response and craete a new JSON
        student_JSON = {
            'id':student['id'],
            'name': student['name'],
            'grade': student['grade']
        } 

        # return the JSON 
        return func.HttpResponse(json.dumps(student_JSON), status_code=200)
    
    # handling the PSOT method
    elif req.method == 'POST':
        # getting the req body
        request_body = req.get_json()
        
        # creating a new student obj from the body
        new_student = {
            'id': request_body.get('id'),
            'name': request_body.get('name'),
            'grade': request_body.get('grade')
        }

        # try persisting the new student to the db
        try: 
            db_collection.insert_one(new_student)
            return func.HttpResponse("New student added successfuly!", status_code=200)
        except:
            return func.HttpResponse("Error persisting new student!!", status_code=400)
    
    # handling the PUT method
    elif req.method == 'PUT':
        # getting the id as a param from URL
        id = req.params.get('id')

        # getting the req body
        request_body = req.get_json()

        # get the student with the id from the db collection
        student = db_collection.find_one({'id': int(id)})

        # updating the student with the new data
        updated_student = {
            '$set': {
                'name': request_body.get('name'),
                'grade': request_body.get('grade')
            }
        }

        # try to update the record
        try: 
            db_collection.update_one(student, updated_student)
            return func.HttpResponse('Student updated successfuly: {}'.format(json.dumps(updated_student)))
        except: 
            return func.HttpResponse("Error updating the student!!", status_code=400)
    
    # handling the DELETE method
    elif req.method == 'DELETE':
        # getting the id as a param from URL
        id = req.params.get('id')

        # get the student with the id from the db collection
        student = db_collection.find_one({'id': int(id)})

        # try to delete the specified student
        try: 
            db_collection.delete_one(student)
            return func.HttpResponse("Student deleted successfuly!", status_code=200)
        except: 
            return func.HttpResponse("Error deleting student!!", status_code=400)
