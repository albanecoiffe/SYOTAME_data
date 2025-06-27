import sys
import cv2
from ultralytics import YOLO

def detect(image_path, model_path='yolov8n.pt'):
    # Charger le modèle YOLO
    model = YOLO(model_path)

    # Lire l'image
    
    image = cv2.imread(image_path)
    if image is None:
        print(f"Erreur : Impossible de lire l'image '{image_path}'")
        return

    image = resize_image(image, size=(640, 320))

    # Lancer la détection
    results = model(image, conf=0.40)


    # Afficher les résultats
    for result in results:
        print("Classes détectées :", result.names)
        print("Boxes détectées :", result.boxes)
        nb_zeros = (result.boxes.cls == 0).sum().item()
        print("Nombre de empty :", nb_zeros)
        nb_ones = (result.boxes.cls == 1).sum().item()
        print("Nombre de occupied :", nb_ones)


        result.plot()  # dessine les boîtes sur l'image
        img_with_boxes = result.plot()

        # Affiche l'image
        cv2.imshow('Detection', img_with_boxes)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def resize_image(image, size=(640, 640)):
    return cv2.resize(image, size, interpolation=cv2.INTER_LINEAR)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Utilisation : python detect.py chemin/vers/image.jpg [chemin/vers/model.pt]")
    else:
        image_path = sys.argv[1]
        model_path = sys.argv[2] if len(sys.argv) > 2 else './models/train6/weights/best.pt'
        detect(image_path, model_path)
