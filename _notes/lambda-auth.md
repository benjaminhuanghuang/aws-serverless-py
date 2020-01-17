## Check auth imformation in http request
```
@app.authorizer()
def basic_auth(auth_request):
    username, password = decode(auth_request.token)
```
## API Gateway API Key
Create API key 

  Usage Plans -> Create API Key and add to Usage Plan

Check API key
```
  @app.route('/todo', api_key_required=True)
  def todos():
    identity = app.current_request.context['identity']
    keyid = identity['apiKeyId']
```

Send HTTP request with API key
```
  x-api-key : <the key>
```

## Cognito
AWS auth service

User management: signup, sign-in

Temporary IAM credentials for AWS access


Create Cognito
```
  aws cloudformation create-stack --stack-name ben-todo-app-auth --capabilities CAPABILITY_IAM --template-body file://congnito.yml
```

```
@app.route('/todo', authorizer=cognito_authorizer)
```