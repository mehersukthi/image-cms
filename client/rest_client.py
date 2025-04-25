import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def create_image():
    print("Creating a new image...")
    data = {
        "title": "Beautiful Mountain",
        "author": "John Doe",
        "image_url": "https://example.com/mountain.jpg",
        "tags": ["nature", "mountain", "landscape"]
    }
    response = requests.post(f"{BASE_URL}/images/", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()


def list_images():
    print("\nListing all images...")
    response = requests.get(f"{BASE_URL}/images/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def get_image(image_id):
    print(f"\nGetting image with ID {image_id}...")
    response = requests.get(f"{BASE_URL}/images/{image_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")


def update_image(image_id):
    print(f"\nUpdating image with ID {image_id}...")
    data = {
        "title": "Updated Mountain View",
        "tags": ["nature", "mountain", "landscape", "updated"]
    }
    response = requests.put(f"{BASE_URL}/images/{image_id}", json=data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")


def delete_image(image_id):
    print(f"\nDeleting image with ID {image_id}...")
    response = requests.delete(f"{BASE_URL}/images/{image_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 204:
        print("Image successfully deleted")
    else:
        print(f"Error: {response.text}")


def filter_images_by_author(author):
    print(f"\nFiltering images by author: {author}...")
    response = requests.get(f"{BASE_URL}/images/?author={author}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def filter_images_by_tag(tag):
    print(f"\nFiltering images by tag: {tag}...")
    response = requests.get(f"{BASE_URL}/images/?tag={tag}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def export_all_images():
    print("\nExporting all images...")
    response = requests.get(f"{BASE_URL}/export/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


if __name__ == "__main__":
    # Create a new image
    image = create_image()
    image_id = image["id"]
    
    # List all images
    list_images()
    
    # Get specific image
    get_image(image_id)
    
    # Update image
    update_image(image_id)
    
    # Filter by author
    filter_images_by_author("John Doe")
    
    # Filter by tag
    filter_images_by_tag("updated")
    
    # Export all images
    export_all_images()
    
    # Delete image
    delete_image(image_id)
    
    # Verify deletion
    list_images()