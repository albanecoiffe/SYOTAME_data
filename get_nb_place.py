import sys
import cv2
from ultralytics import YOLO
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# load secrets from .env file
load_dotenv()

def detect(image, model_path='./models/best.pt'):
    """
    image : image to process, must be image file
    model_path : optionnal, path to the YOLO model file, default is './models/best.pt'

    Load the model from path : `model_path` and detect the number of empty parking spots in the image.

    Return the number of empty parking spots detected in the image.
    If the image is empty or unreadable, return 0.
    """
    # Load the YOLO model
    model = YOLO(model_path)

    # Check if the image is valid
    if image is None:
        print("Erreur : l'image est vide ou illisible")
        return 0

    # Use the model to detect objects in the image, confidence threshold set to 0.25
    results = model(image, conf=0.25)

    # Get result, only 1 image so results is a list with only 1 element
    result = results[0]
    # Count the number of empty parking spots (class 0)
    nb_zeros = (result.boxes.cls == 0).sum().item()
    return nb_zeros

def update_parking_in_db(parking_document, nb_empty):
    """
    parking_document : dict, the parking document to update
    nb_empty : int, the number of empty parking spots detected in the image
    
    Update the parking document in the MongoDB database with the number of empty parking spots.

    Returns nothing.
    """
    # Load the MongoDB API key from environment variables
    api = os.getenv("MONGODB_API")
    uri = f"mongodb+srv://{api}@syotame-db.qopkurw.mongodb.net/?retryWrites=true&w=majority&appName=SYOTAME-DB"

    # Create a MongoClient to connect to the MongoDB database
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    try:
        # Get the database and collection
        db = client["syotame"]
        parking_collection = db["parking"]

        # Update the parking document with the number of empty spots
        parking_document["nbPlaceDispo"] = nb_empty

        # Take the parking id, to check if the document already exists
        pk_id = parking_document["id"]
        # If document already exists, delete it
        existing = parking_collection.find_one({"id": pk_id})
        if existing:
            # Before deleting, updare the number of reserved spots in new document
            parking_document["nbPlaceReserve"] = existing["nbPlaceReserve"]
            parking_collection.delete_one({"_id": existing["_id"]})
        
        # Insert the updated parking document into the collection
        parking_collection.insert_one(parking_document)

    # Deconection 
    finally:
        client.close()

def get_img_api():
    """
    Get the information needed to update the parking document in the database.
    As well as the image to process.

    Returns a tuple (parking_document, image) where:
    - parking_document is a dict with the parking information to update in the database.
    - image is the image to process.
    """
    parking_id="P000"
    parking_document = {
        "id": parking_id,
        "nom" : "Parking village d'Hennemont",
        "adresse":"village d'Hennemont",
        "nbPlaceMax": 12,
        "nbPlaceReserve": 0,
        "geoloc": {"lat": 48.862725, "lon": 2.287592}
    }
    image_path = sys.argv[1]
    image = cv2.imread(image_path)
    return parking_document, image

def use_AI(parking_document,  image):
    """
    parking_document : dict, the parking document to update
    image : image to process, must be image file

    Use existing function to :
        Use the YOLO model to detect the number of empty parking spots in the image.
        Then update the parking document in the database with the number of empty spots.

    Returns nothing.
    """
    model_path = './models/best.pt'
    nb_empty = detect(image, model_path)
    update_parking_in_db(parking_document, nb_empty)

if __name__ == '__main__':
    # Get the parking document and image from function
    parking_document,  image = get_img_api()
    # Use the AI to process the image and update the parking document
    use_AI(parking_document,  image)