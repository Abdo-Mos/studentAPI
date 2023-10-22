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

    if req.method == 'GET':
        stu = db_collection.find_one({'id': 1})
        stu_JSON = {
            'id':stu['id'],
            'name': stu['name'],
            'grade': stu['grade']
        }
        return func.HttpResponse(
            json.dumps(stu_JSON)
        )
        return func.HttpResponse("This is a GET method, and it is working fine")
    elif req.method == 'POST':
        return func.HttpResponse("Now this is a POST and you should do it from POSTMAN!!!")