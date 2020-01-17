from chalice import Chalice

app = Chalice(app_name='todo-app')


TODO_ITEMS = {
    '1': {
        'item': 'buy milk'
    },
    '2': {
        'item': 'mow lawn'
    }
}

@app.route('/')
def index():
    print("Calling our index route")
    return {'hello': 'serverless world'}

@app.route('/todo')
def todos():
    items = [ v for k, v in TODO_ITEMS.items() ]

    params = app.current_request.query_params
    if params:
        offset = int(params.get('offset', 0))
        size = int(params.get('size', len(TODO_ITEMS)))

        return items[offset:size]

    return items

@app.route('/todo/{todo_id}')
def get_todo(todo_id):
    return TODO_ITEMS[todo_id]

@app.route('/todo/{todo_id}', methods=["DELETE"])
def delete_todo(todo_id):
    item = TODO_ITEMS[todo_id]
    del TODO_ITEMS[todo_id]
    return item

@app.route('/todo/{todo_id}', methods=["POST", "PUT"])
def update_todo(todo_id):
    if app.current_request.method == "POST":
        TODO_ITEMS[todo_id].update(app.current_request.json_body)
    else:
        TODO_ITEMS[todo_id] = app.current_request.json_body
    return TODO_ITEMS[todo_id]

@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()

@app.route('/todo', methods=["POST"])
def add_todo():
    todo = app.current_request.json_body
    new_id = str(len(TODO_ITEMS) + 1)
    TODO_ITEMS[new_id] = todo
    return todo

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
