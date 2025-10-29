from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

todolist = []

class Item(BaseModel):
    title: str
    description: str | None = None
    
@app.post("/todos")    
def post(items: Item):
    task = {"title": items.title , "description": items.description}
    todolist.append(task)
    return {"msg": "Task added successfully"}
    


@app.delete("/todos")
def delete(a :int):
    if 0 < a <= len(todolist):
       todolist.pop(a-1)
       return {"msg": f"Task {a} deleted successfully"}
    return {"msg": "Task not found"}



@app.get("/todos")
def show():
    tasks = [{"index": i+1, "title": task["title"], "description": task["description"]}
             for i, task in enumerate(todolist)]
    return {"tasks": tasks}


@app.get("/todos/{a}")
def get(a: int):
    if 0 < a <= len(todolist):
        return {"task": todolist[a-1]}
    return {"msg": "Task not found"}


print ("<< To do list >>")



