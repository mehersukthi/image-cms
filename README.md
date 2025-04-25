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

- **Repository Pattern**: Isolates data access logic
- **Service Layer Pattern**: Encapsulates business logic
- **Dependency Injection**: Used throughout for better testability and loose coupling
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

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

4. Install the dependencies:
```bash
pip install -r requirements.txt
```

5. Generate gRPC code:
```bash
chmod +x scripts/generate_grpc.sh
./scripts/generate_grpc.sh
```

## Running the Application

Start the server:
```bash
python main.py
```

This will start both the REST API server (on port 8000) and the gRPC server (on port 50051).

## Testing the API

### REST API

You can use the provided REST client to test the API:
```bash
python client/rest_client.py
```

Or use tools like Postman or cURL to interact with the endpoints:

- Create an image: `POST http://localhost:8000/api/v1/images/`
- List images: `GET http://localhost:8000/api/v1/images/`
- Get an image: `GET http://localhost:8000/api/v1/images/{image_id}`
- Update an image: `PUT http://localhost:8000/api/v1/images/{image_id}`
- Delete an image: `DELETE http://localhost:8000/api/v1/images/{image_id}`
- Export images: `GET http://localhost:8000/api/v1/export/`

### gRPC API

You can use the provided gRPC client to test the API:
```bash
python client/grpc_client.py
```

## API Documentation

- REST API documentation is available at: `http://localhost:8000/docs`
- gRPC API is defined in the `protos/image_service.proto` file