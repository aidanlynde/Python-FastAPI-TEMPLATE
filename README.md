# slushbrain

Run with **make run**

Build docker with **make build**

Start docker container with **make start**
```
uvicorn app.main:app --host 0.0.0.0 --port 8000

docker build -t my_fastapi_app .

docker run -d -p 8000:8000 my_fastapi_app
```

### Practical Workflow
1. Endpoint Receives Request: Validates and deserializes input using Pydantic schemas.
2. CRUD Function Called: With validated data, performs the required operation in Firestore.
    - If fetching data, it retrieves Firestore documents and converts them into Pydantic schema instances for the response.
    - If writing data, it takes validated data from Pydantic schemas and writes/updates Firestore documents accordingly.



