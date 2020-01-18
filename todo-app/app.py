from chalice import Chalice, NotFoundError, Response, CORSConfig, AuthResponse, AuthRoute
from chalice import CognitoUserPoolAuthorizer

from basicauth import decode
import boto3

app = Chalice(app_name='todo-app')
app.debug = True

dynamodb = boto3.client('dynamodb')
# provider_arns is the UserPoolArn from outputs of the stack created by conginito.yml
cognito_authorizer = CognitoUserPoolAuthorizer(
    'TodoUserPool', header='Authorization',
    provider_arns = ["arn:aws:cognito-idp:us-west-2:173116748583:userpool/us-west-2_FbuRjjjZD"]
)
cors_config = CORSConfig(
  allow_origin="*"
)


TODO_ITEMS = {
    '1': {
        'item': 'buy milk'
    },
    '2': {
        'item': 'mow lawn'
    }
}

@app.authorizer()
def basic_auth(auth_request):
    username, password = decode(auth_request.token)

    if username == password:
        context = {'stripe_user_id': '1234', 'is_admin': True }
        return AuthResponse(routes=['/*'], principal_id=username, context=context)
    return AuthResponse(routes=[], principal_id=None)
        

@app.route('/', authorizer=basic_auth)
def index():
    # read context
    context = app.current_request.context['authorizer']

    print("Calling our index route")
    return {'hello': 'serverless world', 'context' : context }

@app.route('/health')
def health_check():
    # Customize response
    return Response(status_code=200, body="ok\n", headers={'Content-Type': 'text/plain'})

@app.route('/todo', authorizer=cognito_authorizer, cors=cors_config)
def todos():
     
    print("Current user is {}".format(current_user()))

    items = [ v for k, v in TODO_ITEMS.items() ]

    params = app.current_request.query_params
    if params:
        offset = int(params.get('offset', 0))
        size = int(params.get('size', len(TODO_ITEMS)))

        return items[offset:size]

    return items

@app.route('/todo/{todo_id}')
def get_todo(todo_id):
    response = dynamodb.get_item(TableName="chalice-demo", Key={"task_id" : {"S": "task_id"}})
    return response

@app.route('/todo/{todo_id}', methods=["DELETE"])
def delete_todo(todo_id):
    item = TODO_ITEMS[todo_id]
    del TODO_ITEMS[todo_id]
    return item

@app.route('/todo/{todo_id}', methods=["POST", "PUT"])
def update_todo(todo_id):
    dynamodb.put_item(TableName='chalice-demo', Item={})

    if app.current_request.method == "POST":
        TODO_ITEMS[todo_id].update(app.current_request.json_body)
    else:
        TODO_ITEMS[todo_id] = app.current_request.json_body
    return TODO_ITEMS[todo_id]

@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()

@app.route('/todo', methods=["POST"], cors=cors_config)
def add_todo():
    todo = app.current_request.json_body
    new_id = str(len(TODO_ITEMS) + 1)
    TODO_ITEMS[new_id] = todo
    return todo


def current_user():
    auth_context = app.current_request.context.get('authorizer', {})
    return auth_context.get('claims', {}).get('cognito:username')


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
