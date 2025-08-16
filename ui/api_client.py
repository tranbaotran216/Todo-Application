import requests
from url import base_url

#get all todo
def get_todo():
    res = requests.get(f"{base_url}")
    if res.status_code == 200:
        todos = res.json()
        return "\n".join([f"{t['id']}: {t['task']} (done={t['done']})" for t in todos])
    return f"Error: {res.text}"

#post new todo
def add_todo(task):
    res = requests.post(f"{base_url}/", json={"task":task})
    if res.status_code == 200:
        return f"Added: {res.json()}"
    return f"Error: {res.text}"

#put: update todo
def update_todo(todo_id, task, done):
    res = requests.put(f"{base_url}/{todo_id}", json={"task":task, "done":done})
    if res.status_code==200:
        return f"Updated: {res.json()}"
    return f"Error: {res.text}"

#delete
def delete_todo(todo_id):
    res = requests.delete(f"{base_url}/{todo_id}")
    if res.status_code == 200:
        return "deleted successfully"
    return f"Error: {res.text}"

