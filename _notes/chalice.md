

## Error handling



## Response

## CORS
```
from chalice import Chalice, NotFoundError, Response, CORSConfig

cors_config = CORSConfig(
  allow_origin="https://www.example.com"
)

@app.route('/todo', methods=["POST"], cors=cors_config)
```
or 
```
@app.route('/todo', methods=["POST"], cors=True)
```