from typing import Union
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import os
import json
import requests



app = FastAPI()

file_name = "todolist.json"
todolist = []



if os.path.exists(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)
        todolist = data.get("tasks",[])

def saveTask(task):
    todolist.append(task)
    with open("todolist.json", "w", encoding="utf-8") as f:
        data = {"tasks": todolist}
        json.dump(data, f, indent=4, ensure_ascii=False)
        




def rewriteFile():
    with open("todolist.json", "w", encoding="utf-8") as f:
        data = {"tasks": todolist}
        json.dump(data, f, indent=4, ensure_ascii=False)


class Item(BaseModel):
    title: str
    description: str | None = None
    
@app.post("/todos")    
def post(items: Item):
    id = 1
    task = {"id": id, "title": items.title , "description": items.description}
    saveTask(task)
    id = id + 1
    return {"msg": "Task added successfully"}
    


@app.delete("/todos/{index}")
def delete(index: int):
    if 0 < index <= len(todolist):
        todolist.pop(index - 1)
        rewriteFile()
        return {"msg": f"Task {index} deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found"
        )



@app.get("/todos")
def show():
    tasks = [{"id": i+1, "title": task["title"], "description": task["description"]}
             for i, task in enumerate(todolist)]
    return {"tasks": tasks}

@app.get("/todo/{index}")
def get(index: int):
    if 0 < index <= len(todolist):
        task = {"id": index}
        task.update(todolist[index - 1])
        return {"task": task}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found"
        )

@app.get("/request/{seconds}")
def request(seconds: int):
        
    url = f'/api/v1/video/score?duration={seconds}'

    headers = {
        "accept": "application/json",
        "X-Api-Key": ""
    }
    try:
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.ConnectionError:
        return {"error": "ConnectionError"}
    except ValueError:
        return {"error": "Invalid JSON response from server"}
    except Exception as e:
        return {"error": f"Unexpected erro: {str(e)}"}