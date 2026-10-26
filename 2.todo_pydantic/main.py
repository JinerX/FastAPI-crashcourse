from fastapi import FastAPI

from enum import IntEnum
from typing import Optional, List
from pydantic import BaseModel, Field


api = FastAPI()


class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1


# We use pydantic classes to inform FastAPI about the correct input and output structure
class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=512, description='Name of the todo')
    todo_description: str = Field(..., description='Description of todo')
    priority: Priority = Field(default=Priority.LOW, description='Priority of the todo')

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    todo_id: int = Field(..., description='Unique identifier of a todo')

class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512, description='Name of the todo')
    todo_description: Optional[str] = Field(None, description='Description of todo')
    priority: Optional[Priority] = Field(None, description='Priority of the todo')




all_todos = [
    Todo(todo_id=1, todo_name="Clean house", todo_description="Clean the house well", priority=Priority.HIGH),
    Todo(todo_id=2, todo_name="Sports", todo_description="go to the gym", priority=Priority.MEDIUM),
    Todo(todo_id=3, todo_name="Read", todo_description="read at least 10 pages", priority=Priority.LOW),
    Todo(todo_id=4, todo_name="Work", todo_description="Complete documentation", priority=Priority.MEDIUM),
    Todo(todo_id=5, todo_name="Study", todo_description="Review for linear algebra exam", priority=Priority.LOW),
]

def get_todo_index(todo_id):
    i = 0
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return i
        i+=1
    return None


# We add response model to make sure that the output is structured properly
@api.get('/todos/{todo_id}', response_model=Todo)
def get_todo(todo_id): 
    idx = get_todo_index(int(todo_id))
    if idx is None:
        raise ValueError("Invalide todo id")
    return all_todos[idx]


@api.get('/todos', response_model=List[Todo])
def get_todos(first_n: int=None):

    if first_n is not None:
        return all_todos[:first_n]
    else:
        return all_todos


@api.post('/todos', response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo_id = max([todo.todo_id for todo in all_todos]) + 1
    new_todo = Todo(todo_id=new_todo_id, todo_name=todo.todo_name, todo_description=todo.todo_description)
    all_todos.append(new_todo)
    return new_todo


@api.put('/todos/{todo_id}', response_model=Todo)
def edit_todo(todo_id:int, changes:TodoUpdate):
    idx = get_todo_index(todo_id)
    if idx is None:
        raise ValueError("todo_id not found")
    todo = all_todos[idx]
    update_data = changes.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(todo, field, val)
    return todo

@api.delete('/todos/{todo_id}', response_model=List[Todo])
def delete_todo(todo_id:int):
    idx = get_todo_index(todo_id)
    if idx is None:
        raise ValueError("todo idx not found")
    del all_todos[idx]
    return all_todos