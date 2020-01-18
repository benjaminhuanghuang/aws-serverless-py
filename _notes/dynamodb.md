
```
import boto3


dynamodb = boto3.client('dynamodb')
```


## Generate policy
chalice will create policy based on the source code
```
  chalice gen-policy > .chalice/policy-dev.json
```