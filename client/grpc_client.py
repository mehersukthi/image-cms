import grpc
import json
from google.protobuf.json_format import MessageToJson

import image_service_pb2 as pb2
import image_service_pb2_grpc as pb2_grpc


def create_image(stub):
    print("Creating a new image via gRPC...")
    request = pb2.CreateImageRequest(
        image_url="https://example.com/beach.jpg",
        title="Sunset Beach",
        author="Jane Smith",
        tags=["beach", "sunset", "ocean"]
    )
    response = stub.CreateImage(request)
    print(f"Response:\n{MessageToJson(response, indent=2)}")
    return response.image.id


def list_images(stub):
    print("\nListing all images via gRPC...")
    request = pb2.ListImagesRequest(skip=0, limit=100)
    response = stub.ListImages(request)
    print(f"Response:\n{MessageToJson(response, indent=2)}")


def get_image(stub, image_id):
    print(f"\nGetting image with ID {image_id} via gRPC...")
    request = pb2.GetImageRequest(image_id=image_id)
    try:
        response = stub.GetImage(request)
        print(f"Response:\n{MessageToJson(response, indent=2)}")
    except grpc.RpcError as e:
        print(f"Error: {e.details()}")


def update_image(stub, image_id):
    print(f"\nUpdating image with ID {image_id} via gRPC...")
    request = pb2.UpdateImageRequest(
        image_id=image_id,
        title="Updated Beach Sunset",
        tags=["beach", "sunset", "ocean", "updated"]
    )
    try:
        response = stub.UpdateImage(request)
        print(f"Response:\n{MessageToJson(response, indent=2)}")
    except grpc.RpcError as e:
        print(f"Error: {e.details()}")


def delete_image(stub, image_id):
    print(f"\nDeleting image with ID {image_id} via gRPC...")
    request = pb2.DeleteImageRequest(image_id=image_id)
    try:
        response = stub.DeleteImage(request)
        print(f"Success: {response.success}")
    except grpc.RpcError as e:
        print(f"Error: {e.details()}")


def filter_images_by_author(stub, author):
    print(f"\nFiltering images by author: {author} via gRPC...")
    request = pb2.ListImagesRequest(skip=0, limit=100, author=author)
    response = stub.ListImages(request)
    print(f"Response:\n{MessageToJson(response, indent=2)}")


def filter_images_by_tag(stub, tag):
    print(f"\nFiltering images by tag: {tag} via gRPC...")
    request = pb2.ListImagesRequest(skip=0, limit=100, tag=tag)
    response = stub.ListImages(request)
    print(f"Response:\n{MessageToJson(response, indent=2)}")


def export_all_images(stub):
    print("\nExporting all images via gRPC...")
    request = pb2.ExportImagesRequest()
    response = stub.ExportImages(request)
    print(f"Response:\n{MessageToJson(response, indent=2)}")


if __name__ == "__main__":
    # Create a gRPC channel
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client)
        stub = pb2_grpc.ImageServiceStub(channel)
        
        # Create a new image
        image_id = create_image(stub)
        
        # List all images
        list_images(stub)
        
        # Get specific image
        get_image(stub, image_id)
        
        # Update image
        update_image(stub, image_id)
        
        # Filter by author
        filter_images_by_author(stub, "Jane Smith")
        
        # Filter by tag
        filter_images_by_tag(stub, "updated")
        
        # Export all images
        export_all_images(stub)
        
        # Delete image
        delete_image(stub, image_id)
        
        # Verify deletion
        list_images(stub)