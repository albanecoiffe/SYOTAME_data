# Connexion (tu l'as déjà)
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://LG:U55Ltdc.pB7PMuj@syotame-db.qopkurw.mongodb.net/?retryWrites=true&w=majority&appName=SYOTAME-DB"
client = MongoClient(uri, server_api=ServerApi('1')) #server_api=ServerApi('1') demande a MongoDB de fournir une interface compatible avec la version 1 de l’API. Garantit que le code reste compatible dans le futur même si l’API évolue 

try:
    # Création de la base de données et des collections
    db = client["syotame"]  # nom de la base de données
    parking_collection = db["parking"]
    user_collection = db["user"]

    # Exemple de document pour parking qu'on ajoute dans la bdd (il faut toutes les informations car il faut respecter 
    # la structure pour chaque, donc il faut A CHAQUE FOIS donc que chaque document est cette structure
    
    """
    exemple de structure d'un document parking:
    parking_document = {
        "id": "P001",
        "nbPlaceMax": 100,
        "nbPlaceDispo": 40,
        "geoloc": {"lat": 48.8566, "lon": 2.3522},
        "nbPlaceReserve": 60
    }
    """
    #Un document qui sera inséré pour avoir autre chose que le vide mais attention un document peut être inséré plusieurs fois donc à supprimer 
    parking_document = {
        "id": "P000",
        "nbPlaceMax": 0,
        "nbPlaceDispo": 0,
        "geoloc": {"lat": 27.9879017, "lon": 86.9253141},
        "nbPlaceReserve": 0
    }
    # Exemple de document pour user qu'on ajoute dans la bdd
    """
    exemple de structure d'un document user
    user_document = {
        "id": "U001",
        "reservation": ["P001", "P003"]  # liste d'IDs de parkings réservés
    }
    """
    #Un document qui sera inséré pour avoir autre chose que le vide mais attention un document peut être inséré plusieurs fois donc à supprimer 
    user_document = {
        "id": "U00",
        "reservation": []  # liste d'IDs de parkings réservés
    }
    # Insertion des documents créers dans la bdd
    parking_collection.insert_one(parking_document)
    user_collection.insert_one(user_document)

    #Lire tous les parkings 
    for p in parking_collection.find():
        print("Infor parking: ",p)

    #Trouver un parking par son ID
    parking = parking_collection.find_one({"id": "P001"})
    print("Je t'ai trouve par ton ID parking: ",parking)

    #Trouver un user par son id
    user = user_collection.find_one({"id": "U001"})
    print("Avoir un user par l'id: ",user)


    #Si on veut éviter les doublons dans la bdd, on utilse "if not avec l'id de ce qu'on insert"
    # if not parking_collection.find_one({"id": "P001"}):
    #     parking_collection.insert_one(parking_document)

#Pour se deconnecter, la partie rse de la bdd pour éviter une connexion prolongée
finally:
    client.close()  #Ferme la connexion