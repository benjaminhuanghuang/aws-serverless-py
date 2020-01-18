class TodoDB:
    def __init__(self):
        self.todos = {
            '1': {
                'item': 'buy milk'
            },
            '2': {
                'item': 'mow lawn'
            }
        }

    def get_todos(self):
        return [ v for k, v in self.todos.items() ]
    
    def get_todo(self, todo_id):
        if todo_id in self.todos:
            return self.todos[todo_id]
        return None

    def delete_todo(self, todo_id):
        item = self.todos[todo_id]
        del self.todos[todo_id]
        return item
    
    def update_todo(self, todo_id, todo_info):
        self.todos[todo_id].update(todo_info)
    
    def replace_todo(self, todo_id, todo):
        self.todos[todo_id] = todo
    
    def add_todo(self, todo):
        new_id = str(len(self.todos) + 1)
        self.todos[new_id] = todo
        return todo        
