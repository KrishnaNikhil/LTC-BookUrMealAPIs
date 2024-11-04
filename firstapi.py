from fastapi import FastAPI, Header,HTTPException
from pydantic import BaseModel
from typing import Annotated, List
import jwt
import pymongo
import logging
from bson import json_util
import json
import pymongo.collation
import pymongo.collection
import uvicorn
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId

app = FastAPI()
logger = logging.getLogger('uvicorn.error')
class Task(BaseModel):
	title: str
	description: str = ""

class GenToken(BaseModel):
	userId: str
	pwd: str

class RegisterUser(BaseModel):
	email: str
	pwd: str
	userType: str

class MenuCard(BaseModel):
	commonItems:str
	nonVegItems:str
	vegItems:str
	
class Order(BaseModel):
	menuItems:str
	userId:str	



tasks = []
dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
dataBase = dbclient["BookUrMeal"]


@app.get("/getLast7DaysOrders/{emailId}")
def getTodaysMenu(emailId:str): 
	mdMenus = dataBase["Orders"]
	todayDt = datetime.today()
	query = {"$and": [{"createdOn": {"$gte": (todayDt - timedelta(days=7)).strftime('%Y-%m-%d'), "$lte": todayDt.strftime('%Y-%m-%d')}}, {"userId": emailId}]}
	print(query)
	resp = "{\"orders\":["
	resultSet = mdMenus.find(query)
	
	firstDoc : bool = True
	for document in resultSet:
		print(document)
		del document["_id"]
		if firstDoc:
			resp = resp+json.dumps(document)
			firstDoc = False
		else:
			resp = resp+","+json.dumps(document)
		
	resp = resp+"]}"
	res = json.loads(resp)
	print(str(res))
	return res
	# print(json.dumps(finaldict))

	# return CusJSONEncoder().encode(finaldict)

class CusJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.post("/createOrder/")
def createOrder(order: Order): 
	print(order)
	mdOrders = dataBase["Orders"]
	orderID = datetime.today().strftime('%Y%m%d%H%M%S%s')
	result = {"msg": "Order placed succesfully","orderID": orderID}
	orderDict = order.__dict__
	orderDict['orderID'] = orderID
	orderDict['createdOn'] = datetime.today().strftime('%Y-%m-%d')
	x = mdOrders.insert_one(orderDict)
	return result

@app.get("/getTodaysMenu")
def getTodaysMenu(): 
	mdMenus = dataBase["Menus"]
	query = { "createdOn": datetime.today().strftime('%Y-%m-%d') }
	print(query)
	resultSet = mdMenus.find_one(query)
	del resultSet["_id"]
	print(type(resultSet))
	return resultSet

@app.post("/addItemsOnTodaysMenu/")
def addItemsOnTodaysMenu(menuCard: MenuCard): 
	print(menuCard)

	mdMenus = dataBase["Menus"]
	menudict = menuCard.__dict__
	
	menudict['createdOn'] = datetime.today().strftime('%Y-%m-%d')
	print(menudict)
	mdMenus.insert_one(menudict)
	result = {"msg": "Menu added succesfully"}
	
	return result
	
@app.put("/updateItemsOnTodaysMenu")
def updateItemsOnTodaysMenu(updtmenuCard: MenuCard): 
	mdMenus = dataBase["Menus"]
	updmenudict = updtmenuCard.dict(exclude_unset=True)
	menuDt = datetime.today().strftime('%Y-%m-%d')
	print(menuDt)
	mdMenus.update_one({"createdOn": menuDt},{"$set":updmenudict})
	result = {"msg": "Menu updated succesfully"}
	return result

@app.post("/registerUser/")
def registerUser(regUser: RegisterUser): 
	mdUsers = dataBase["Users"]
	result = {"msg": "Registered user succesfully"}
	x = mdUsers.insert_one(regUser.__dict__)
	return result

@app.get("/getProfileDetails/{emailId}")
def registerUser(emailId:str): 
	mdUsers = dataBase["Users"]
	query = { "email": emailId }
	resultSet = mdUsers.find_one(query)
	del resultSet["_id"]
	return resultSet

@app.post("/generateToken/")
def generateToken(tokenPayload: GenToken):
	  
	header = {  
	"alg": "HS256",  
	"typ": "JWT"  
	}
	encoded_jwt = jwt.encode(tokenPayload.__dict__ , "123456", algorithm='HS256', headers=header)  
	# tokens.append(encoded_jwt)
	mdTokens = dataBase["Tokens"]
	result = {"msg": "Token generated succesfully",
		 "Token": encoded_jwt}
	x = mdTokens.insert_one({"token":encoded_jwt})
	return result
	

@app.post("/tasks/")
def create_task(task: Task):
	tasks.append(task)
	return {"msg": "task added succesfully"}
@app.get("/tasks/", response_model=List[Task])
def get_tasks():
	return tasks
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
	if 0 <= task_id < len(tasks):
		return tasks[task_id]
	else:
		raise HTTPException(status_code=404, detail="Task not found")
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
	if 0 <= task_id < len(tasks):
		tasks[task_id] = updated_task
		return updated_task
	else:
		raise HTTPException(status_code=404, detail="Task not found")
	
@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
	if 0 <= task_id < len(tasks):
		deleted_task = tasks.pop(task_id)
		return deleted_task
	else:
		raise HTTPException(status_code=404, detail="Task not found")


if __name__ == "__main__":
	uvicorn.run(app, host="192.168.29.243", port=8000)
