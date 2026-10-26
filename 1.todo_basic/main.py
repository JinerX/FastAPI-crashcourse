from fastapi import FastAPI

api = FastAPI()







all_todos = [
    {'todo_id': 1, 'todo_name': 'Sports', 'todo_description': 'Go to the gym'},
    {'todo_id': 2, 'todo_name': 'Read', 'todo_description': '10 pages'},
    {'todo_id': 3, 'todo_name': 'Shop', 'todo_description': 'meat, cucumber, ...'},
    {'todo_id': 4, 'todo_name': 'Do the dishes', 'todo_description': 'Do then'},
    {'todo_id': 5, 'todo_name': 'Study', 'todo_description': '1h of linear algebra revision'},
]

def get_todo_index(todo_id):
    i = 0
    for todo in all_todos:
        if todo["todo_id"] == todo_id:
            return i
        i+=1
    return None


# path parameters
@api.get('/todos/{todo_id}') # we can use the parameter in curly brackets in the funciton
def get_todo(todo_id): # parameter user passes is passed to the function as an input, function arg names need to match the parameter names
    idx = get_todo_index(int(todo_id))
    return all_todos[idx] # the parameters are passed as a string

@api.get('/todos/{todo_id}/{entry}')
def get_entry(todo_id, entry):
    idx = get_todo_index(int(todo_id))
    return all_todos[idx][entry]

# query parameters - not specified in the path, but after ?
#here localhost:port:todos?first_n=val
@api.get('/todos')
def get_todos(first_n: int=None): #:int does influence the fastapi's internals

    if first_n is not None:
        return all_todos[:first_n]
    else:
        return all_todos

# # combining path and query parameters - just for testing
# @api.get('/todos2/{todo_id}')
# def get_entry(todo_id:int , entry:str = None):
#     if entry:
#         return all_todos[todo_id][entry]
#     else:
#         return all_todos[todo_id]

# # localhost:.../todos2/1?entry=todo_name - works


@api.post('/todos')
def create_todo(todo: dict):
    new_todo_id = max([todo['todo_id'] for todo in all_todos]) + 1
    new_todo = {
        'todo_id': new_todo_id,
        'todo_name': todo['todo_name'],
        'todo_description': todo['todo_description']
    }
    all_todos.append(new_todo)
    return new_todo

# test out the post by going to /docs

@api.put('/todos/{todo_id}')
def edit_todo(todo_id:int, todo_entry, todo_val):
    idx = get_todo_index(todo_id)

    valid_entries = all_todos[0].keys()
    if todo_entry not in valid_entries:
        return {"error_type": "invalid todo entry"}
    if todo_entry and todo_val:
        all_todos[idx][todo_entry] = todo_val
    return all_todos[idx]

@api.delete('/todos/{todo_id}')
def delete_todo(todo_id:int, todo_entry=None):
    idx = get_todo_index(todo_id)
    
    valid_entries = all_todos[0].keys()
    if todo_entry:
        if todo_entry not in valid_entries: 
            return {"error_type": "invalid todo entry"}
        all_todos[idx][todo_entry] = ''
        return all_todos[idx]
    else:
        del all_todos[idx]
    return all_todos