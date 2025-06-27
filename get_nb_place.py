import sys
import cv2
from ultralytics import YOLO
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

def detect(image_path, model_path='yolov8n.pt'):
    model = YOLO(model_path)

    if image is None:
        print(f"Erreur : Impossible de lire l'image '{image_path}'")
        return

    results = model(image, conf=0.25)

    result = results[0]
    nb_zeros = (result.boxes.cls == 0).sum().item()
    return nb_zeros

def update_parking_in_db(parking_document, nb_empty):
    uri = os.getenv("MONGODB_URI")
    client = MongoClient(uri, server_api=ServerApi('1')) #server_api=ServerApi('1') demande a MongoDB de fournir une interface compatible avec la version 1 de l’API. Garantit que le code reste compatible dans le futur même si l’API évolue 

    try:
        # Création de la base de données et des collections
        db = client["syotame"]  # nom de la base de données
        parking_collection = db["parking"]

        parking_document["nbPlaceDispo"] = nb_empty
        pk_id = parking_document["id"]
        # Si un document avec le même parking id existe, on le supprime
        existing = parking_collection.find_one({"id": pk_id})
        if existing:
            parking_collection.delete_one({"_id": existing["_id"]})

        parking_collection.insert_one(parking_document)

    #Pour se deconnecter, la partie rse de la bdd pour éviter une connexion prolongée
    finally:
        client.close()  #Ferme la connexion

def get_img_api():
    parking_id="P000"  # ID du parking à mettre à jour
    parking_document = {
        "id": parking_id,
        "nbPlaceMax": 12,
        "geoloc": {"lat": 48.862725, "lon": 2.287592},
        "nbPlaceReserve": 0
    }
    image_path = sys.argv[1]
    image = cv2.imread(image_path)
    return parking_document, image

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Utilisation : python detect.py chemin/vers/image.jpg [chemin/vers/model.pt]")
    else:
        model_path = sys.argv[2] if len(sys.argv) > 2 else './models/train6/weights/best.pt'
        parking_document,  image = get_img_api()
        nb_empty = detect(image, model_path)
        update_parking_in_db(parking_document, nb_empty)


    
