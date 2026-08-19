import json

def load_data():
    with open("todos.json", "r")as file:
        data = json.load(file)
        return data
    
def save_data(data):
    with open("todos.json","w")as file:
        json.dump(data,file)   