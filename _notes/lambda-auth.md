## Check auth imformation in http request
```
@app.authorizer()
def basic_auth(auth_request):
    username, password = decode(auth_request.token)
```
## API Gateway

## Cognito
AWS auth service

User management: signup, sign-in

Temporary IAM credentials for AWS access