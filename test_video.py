import sys
import cv2
from ultralytics import YOLO
import os

def detect_and_save_video(video_path, model_path='yolov8n.pt', output_path='output_detected.mp4'):
    # Charger le modèle YOLO
    model = YOLO(model_path)

    # Ouvrir la vidéo
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Erreur : Impossible d'ouvrir la vidéo '{video_path}'")
        return

    # Obtenir les dimensions et le framerate de la vidéo d'entrée
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Créer un writer pour enregistrer la vidéo de sortie
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # ou 'XVID' pour .avi
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # fin de la vidéo


        # Détection sur la frame
        results = model(frame, conf=0.40)

        for result in results:
            nb_zeros = (result.boxes.cls == 0).sum().item()
            nb_ones = (result.boxes.cls == 1).sum().item()
            print("Nombre de 'empty' :", nb_zeros)
            print("Nombre de 'occupied' :", nb_ones)

            # Annoter l'image
            frame_with_boxes = result.plot()

        # Sauvegarder
        out.write(frame_with_boxes)

    cap.release()
    out.release()
    print(f"Vidéo enregistrée sous : {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Utilisation : python detect_video.py chemin/vers/video.mp4 [chemin/vers/model.pt]")
    else:
        video_path = sys.argv[1]
        model_path = sys.argv[2] if len(sys.argv) > 2 else './models/train6/weights/best.pt'

        # Construire le chemin de sortie
        filename = os.path.basename(video_path)
        name, _ = os.path.splitext(filename)
        output_file = f"./demo/{name}_detected.mp4"

        detect_and_save_video(video_path, model_path, output_path=output_file)
