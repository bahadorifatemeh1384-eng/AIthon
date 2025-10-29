from typing import Union

from fastapi import FastAPI

app = FastAPI()

todolist = []


class Todo:

    def __init__(self, title, description):

        self.title = title
        self.description = description

    
    def manage_add(self):
        todolist.append(task)
        return {"msg": "Task added successfully"}
    

    def manage_delete(index :int):
        if 0 < index <= len(todolist):
           todolist.pop(index-1)
           return {"msg": f"Task {index} deleted successfully"}
        return {"msg": "Task not found"}


    def manage_show():
        return {f" {index + 1} . title:{task.title} \n description: {task.description}"}
     

    def manage_get(index :int):
        if 0 < index <= len(todolist):
            return todolist[index-1]
        return {"msg": "Task not found", "error": "Invalid task index"}
    

@app.post("/todos/{title}/{description}")
def add ():
    task = Todo(title, description)
    task.manage_add()


@app.delete("/todos/{index}")
def delete():
    Todo.manage_delete()


@app.get("/todos")
def show():
    Todo.manage_show()


@app.get("/todos/{index}")
def get(index: int):
    Todo.manage_get(index)

