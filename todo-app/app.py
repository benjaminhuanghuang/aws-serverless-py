from chalice import Chalice, NotFoundError, Response, CORSConfig, AuthResponse, AuthRoute, CognitoUserPoolAuthorizer
from basicauth import decode
import os
from chalicelib.tododb import TodoDB

app = Chalice(app_name='todo-app')
app.debug = True

cognito_authorizer = CognitoUserPoolAuthorizer(
    'TodoUserPool', header='Authorization',
    provider_arns=[os.getenv("USER_POOL_ARN")]
)

cors_config = CORSConfig(
  allow_origin="*"
)


TODO_DB = TodoDB()

@app.authorizer()
def basic_auth(auth_request):
    username, password = decode(auth_request.token)

    if username == password:
        context = {'stripe_user_id': '1234', 'is_admin': True }
        return AuthResponse(routes=['/*'], principal_id=username, context=context)
    return AuthResponse(routes=[], principal_id=None)
        

@app.route('/', authorizer=basic_auth)
def index():
    context = app.current_request.context['authorizer']

    print("Calling our index route")
    return {'hello': 'serverless world', 'context' : context }

@app.route('/health')
def health_check():
    msg = "ok\nTODO_MAX_ITEMS={}".format(os.getenv("TODO_MAX_ITEMS"))
    return Response(status_code=200, body=msg, headers={'Content-Type': 'text/plain'})

def current_user():
    auth_context = app.current_request.context.get('authorizer', {})
    return auth_context.get('claims', {}).get('cognito:username')


@app.route('/todo', authorizer=cognito_authorizer, cors=cors_config)
def todos():

    print("Current user is {}".format(current_user()))

    items = TODO_DB.get_todos()

    params = app.current_request.query_params
    if params:
        offset = int(params.get('offset', 0))
        size = int(params.get('size', len(TODO_ITEMS)))

        return items[offset:size]

    return items

@app.route('/todo/{todo_id}')
def get_todo(todo_id):
    todo = TODO_DB.get_todo(todo_id)
    if todo:
        return todo
    raise NotFoundError

@app.route('/todo/{todo_id}', methods=["DELETE"])
def delete_todo(todo_id):
    return TODO_DB.delete_todo(todo_id)

@app.route('/todo/{todo_id}', methods=["POST", "PUT"])
def update_todo(todo_id):
    if app.current_request.method == "POST":
        TODO_DB.update(todo_id, app.current_request.json_body)
    else:
        TODO_DB.replace(todo_id, app.current_request.json_body)
    return TODO_DB.get_todo(todo_id)

@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()

@app.route('/todo', methods=["POST"], cors=cors_config)
def add_todo():
    todo = app.current_request.json_body
    return TODO_DB.add_todo(todo)

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#

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
