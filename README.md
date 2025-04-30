# Image CMS API

A platform to support content management systems for images (CMS). This application provides both REST and gRPC APIs for CRUD operations on images, along with an export feature.

## Features

- Public REST API for CRUD operations on images
- High-performance gRPC API for system-to-system communication
- SQLite database for persistent storage
- Image filtering by author and tags
- Export functionality with optional filters

## Project Structure

The project follows a layered architecture design:

1. **API Layer**: REST (FastAPI) and gRPC endpoints
2. **Service Layer**: Business logic
3. **Repository Layer**: Data access and manipulation
4. **Model Layer**: Database models and schemas

## Design Patterns

- **Facade Pattern**: Isolates data access logic (Repository layer)
- **Factory Pattern**: Used for creating database connections

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd image-cms
```

2. Install the dependencies:
```bash
pip install -r requirements.txt
```

5. Generate gRPC code:
```bash
chmod +x scripts/generate_grpc.sh
./scripts/generate_grpc.sh
```
This will create image_services_pb2_grpc.py and image_service_pb2.py in the root 

## Running the Application

Start the server:
```bash
python main.py
```
main.py is the single point entry to start both rest api server and grpc server. 
This will start both the REST API server (on port 8000) and the gRPC server (on port 50051).

## Testing the API

### REST API

You can use the provided REST client to test the API:
```bash
python client/rest_client.py
```

Or use tools like Postman or cURL to interact with the endpoints:

Create an image: POST http://localhost:8000/api/v1/images/
List Images with Filters: GET http://localhost:8000/api/v1/images?author={author}&tag={tag}
List images: GET http://localhost:8000/api/v1/images/
Get an image: GET http://localhost:8000/api/v1/images/{image_id}
Update an image: PUT http://localhost:8000/api/v1/images/{image_id}
Delete an image: DELETE http://localhost:8000/api/v1/images/{image_id}
Export images: GET http://localhost:8000/api/v1/export/

Examples executions of API:

- Create an image: `POST http://localhost:8000/api/v1/images/`
  Example post JSON body:
  {
  "title": "Beautiful Mountain",
  "author": "John Doe",
  "image_url": "https://example.com/mountain.jpg",
  "tags": ["nature", "mountain", "landscape"]
  }
  
- List Images with Filters: `GET http://localhost:8000/api/v1/images?author={author}&tag={tag}` 

  Request: http://localhost:8000/api/v1/images?tag=serene
  Response: 200 OK 
  [
    {
        "id": 3,
        "title": "Beautiful Mountain",
        "author": "John Doe",
        "tags": [
            "serene",
            "mountain",
            "landscape"
        ],
        "created_at": "2025-04-26T23:56:05.251850"
    }
]

- List images: `GET http://localhost:8000/api/v1/images/`
Response : 200 Ok
[
    {
        "id": 1,
        "title": "Beautiful Mountain",
        "author": "John Doe",
        "tags": [
            "nature",
            "mountain",
            "landscape"
        ],
        "created_at": "2025-04-25T22:16:40.198863"
    },
    {
        "id": 2,
        "title": "Beautiful Mountain",
        "author": "John Doe",
        "tags": [
            "nature",
            "mountain",
            "landscape"
        ],
        "created_at": "2025-04-26T23:49:20.489390"
    },
    {
        "id": 3,
        "title": "Beautiful Mountain",
        "author": "John Doe",
        "tags": [
            "serene",
            "mountain",
            "landscape"
        ],
        "created_at": "2025-04-26T23:56:05.251850"
    }
]
- Get an image: `GET http://localhost:8000/api/v1/images/{image_id}`
  Request: http://localhost:8000/api/v1/images/1

- Update an image: `PUT http://localhost:8000/api/v1/images/{image_id}`
  Request: http://localhost:8000/api/v1/images/2
  Request Body:  
  {
  "title": "mystery Mountain",
  "author": "chetan Bhagat",
  "image_url": "https://example.com/mountain.jpg",
  "tags": ["crime", "thriller", "intense"]
  }
  Response: 200 OK 
  {
    "title": "mystery Mountain",
    "author": "chetan Bhagat",
    "image_url": "https://example.com/mountain.jpg",
    "id": 2,
    "created_at": "2025-04-26T23:49:20.489390",
    "tags": [
        {
            "tag": "crime",
            "id": 10,
            "image_id": 2
        },
        {
            "tag": "thriller",
            "id": 11,
            "image_id": 2
        },
        {
            "tag": "intense",
            "id": 12,
            "image_id": 2
        }
    ]
}
- Delete an image: `DELETE http://localhost:8000/api/v1/images/{image_id}`
 Request: http://localhost:8000/api/v1/images/2
 Response: 204 No content 

- Export images: `GET http://localhost:8000/api/v1/export/`
Response:

[
    {
        "title": "Beautiful Mountain",
        "author": "John Doe",
        "image_url": "https://example.com/mountain.jpg",
        "id": 3,
        "created_at": "2025-04-26T23:56:05.251850",
        "tags": [
            {
                "tag": "serene",
                "id": 7,
                "image_id": 3
            },
            {
                "tag": "mountain",
                "id": 8,
                "image_id": 3
            },
            {
                "tag": "landscape",
                "id": 9,
                "image_id": 3
            }
        ]
    }
]

### gRPC API

You can use the provided gRPC client to test the API:
```bash
python client/grpc_client.py
```

## API Documentation

- REST API documentation is available at: `http://localhost:8000/docs`
- gRPC API is defined in the `protos/image_service.proto` file

------------------------------------------------------------------------------------

The flow of the application and implementation goes as follows for any code reader to understand how everything works:

1. when the developer starts the application with python main.py it creates AppServer instance and starts the actual server which is in /app/core/server.py
2. This AppServer uses the RESTAPI controller router in /app/api/rest/images.py /app/api/rest/export.py and GRPC SERVER in /app/api/grpc/server.py and starts both the rest server (uvicorn fast api) and grpc server and Creates database tables using SQLAlchemy’s Base.metadata.create_all().
3. REST server starts (Uvicorn) runs on http://localhost:8000 and includes:
Auto-generated Swagger UI at /docs for interactive testing and Dependency-injected routes (get_db injects database sessions into endpoints).
4. GRPC server runs and Attaches the ImageServiceServicer (implemented in app/api/grpc/services/images.py) to handle gRPC methods defined in image_service.proto
5.  REST Request Flow
Client -> FastAPI Router (e.g., POST /api/v1/images/).
Router validates input using Pydantic schemas (ImageCreate, ImageUpdate).
Dependency Injection provides a database session (get_db).
Service Layer (ImageService) processes business logic (e.g., applying filters for GET requests).
Repository Layer (ImageRepository) executes SQL operations via SQLAlchemy.
Database (SQLite) persists data in images and image_tags tables.
6. gRPC Request Flow
Client calls a gRPC method (e.g., CreateImage).
gRPC Servicer (ImageServiceServicer):
Translates Protobuf messages to Python objects.
Reuses the same ImageService as the REST API.
Service/Repository Layers handle logic identically to REST.

