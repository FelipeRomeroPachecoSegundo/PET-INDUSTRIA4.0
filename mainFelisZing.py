# Importando as bibliotecas necessárias
import cv2 as cv
import anacPitalista

# A main é utilizada para chamar os métodos da aplicação
#camera = cv.VideoCapture(0)
camera = cv.VideoCapture(0)  # URL da Camera do telefone
ret1, img1 = camera.read()
anacPitalista.monitorarArea(camera)
camera.release()
cv.destroyAllWindows()

