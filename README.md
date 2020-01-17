# aws-serverless-py

## Reference
-[ Deploying REST Services with Chalice for AWS](https://www.linkedin.com/learning/deploying-rest-services-with-chalice-for-aws)


## Chalice
Chalic is a python framework for AWS serverless app

Chalicd handles API gateway provision, deploynet, configuration

Provide API to S3, SNS, SQS

## Setup
Install chalic
```
  python3 -m venv venv3

  . venv3/bin/activate

  pip install chalic

  chalic --help
```
Setup aws cridentials
```
  pip install awscli

  aws configure     # input aws access key and secret access key
``` 

Test, get current user
```
  aws sts get-caller-identity
```

Create chalice app
```
chalice new-project todo-app

```

Run app
```
  chalice local
```

Deploy chalice app
```
  chalice deploy
```

Check log
```
  chalice logs --stage dev
```