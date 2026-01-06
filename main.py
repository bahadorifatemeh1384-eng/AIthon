from typing import Union
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import os
from decouple import config

import json
import requests
import logging


logging.basicConfig(
    filename="info.log",
    level=logging.INFO,
    # format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("service-logger")


app = FastAPI()

file_name = "todolist.json"
todolist = []



if os.path.exists(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)
        todolist = data.get("tasks",[])

def saveTask(task):
    try:
        todolist.append(task)
        rewriteFile()

        logger.info("Task saved successfully" )
        
    except Exception as e:
        logger.error(f"Failed to save task | error={e}")
        raise


def rewriteFile():
    with open(file_name, "w", encoding="utf-8") as f:
        data = {"tasks": todolist}
        json.dump(data, f, indent=4, ensure_ascii=False)


class Item(BaseModel):
    title: str
    description: str | None = None
    
@app.post("/todos")    
def post(items: Item):
    logger.info("post /todos called")

    id = 1
    task = {"id": id, "title": items.title , "description": items.description}
        
    try:
        saveTask(task)
        id = id + 1

        logger.info("Task add successfully")
        return {"msg": "Task added successfully"}   


    except Exception as e:
        logger.error(f"Failed to add task | error={e}")
        return {"msg": "Failed to add task"}, 500


@app.delete("/todos/{index}")
def delete(index: int):
    logger.info("delete /todos called")

    if 0 < index <= len(todolist):
        todolist.pop(index - 1)
        rewriteFile()

        logger.info("Task deleted successfuly")
        return {"msg": f"Task {index} deleted successfully"}
    
    else:
        logger.error("Failed ti delete task | error= ")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found"
        )



@app.get("/todos")
def show():
    logger.info("GET /todos called")

    tasks = [{"id": i+1, "title": task["title"], "description": task["description"]}
            for i, task in enumerate(todolist)]
        
    return {"tasks": tasks}

@app.get("/todo/{index}")
def get(index: int):
    logger.info("GET /todo{index} called")

    if 0 < index <= len(todolist):
        task = {"id": index}
        task.update(todolist[index - 1])
        logger.info(f"Task found | id={index} | title={task.get('title')}")
        return {"task": task}
    else:
        logger.warning(f"Task not found | id={index}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found"
        )

@app.get("/request/{seconds}")
def request(seconds: int):
    logger.info("get /request{seconds} called")
        
    url = f'{config("DIDIMOON_SCORE_DOMAIN")}/api/v1/video/score?duration={seconds}'

    headers = {
        "accept": "application/json",
        "X-Api-Key": config("DIDIMOON_SCORE_API_KEY"),
    }
    try:
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.ConnectionError:
        logger.error("connection error")
        return {"error": "ConnectionError"}
    except ValueError:
        logger.error("Invalid JSON response from server")
        return {"error": "Invalid JSON response from server"}
    except Exception as e:
        logger.error(f" error={e}")
        return {"error": f"Unexpected erro: {str(e)}"}