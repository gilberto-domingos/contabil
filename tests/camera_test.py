import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Câmera não encontrada ou em uso.")
else:
    print("Câmera conectada com sucesso.")
cap.release()
