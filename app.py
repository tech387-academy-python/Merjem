from flask import Flask, request, json, Response
from pymongo import MongoClient

app = Flask(__name__)


class MongoAPI:
    def __init__(self, data):
        self.client = MongoClient("mongodb://settingup_mymongo_1_1:27017")  
      
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data


    def read(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

     
    def write(self, data):
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output


    def update(self):
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output      

    def delete(self, data):
        filt = data['Document']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output



data = {
        "database": "MerjemDB",
        "collection": "people",
    }

@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')


@app.route('/mongodb', methods=['GET'])
def mongo_read():

    data = {
        "database": "MerjemDB",
        "collection": "people",
    }

    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.read()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')    


@app.route('/mongodb', methods=['POST'])
def mongo_write():
    data = {
        "database":"MerjemDB",
        "collection":"people",
        "Document":{
            "First_Name": "John",
            "Age": 50
        }
    }
    if data is None or data == {} or 'Document' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.write(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')



@app.route('/mongodb', methods=['PUT'])
def mongo_update():
    data = {
        "database": "MerjemDB",
        "collection": "people",
        "Filter": {
            "first_name":"Samira"
        },
        "DataToBeUpdated": {
            "Last_Name": "Jdaic",
            "Age":73
        }

    }

    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.update()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')





@app.route('/mongodb', methods=['DELETE'])
def mongo_delete():
    data = {
        "database": "MerjemDB",
        "collection": "people",
        "Filter": {
            "First_Name": "John"
        }
        }
    
    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.delete(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='localhost')
  


