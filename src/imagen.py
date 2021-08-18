import cv2 as cv
import numpy as np

# Clase que contiene todos los métodos del procesamiento de imágenes
class Imagen(object):
  def __init__(self, imagen):
    # abrir la imagen con cv2
    self.imagen_original = cv.imread(imagen)

    # verificamos que la imagen se puede abrir
    if self.imagen_original is None:
      raise IOError('No se puede abrir la imagen')
    
    # 1 - Pasar a escala de grises
    gris = cv.cvtColor(self.imagen_original, cv.COLOR_BGR2GRAY)

    # 2 - Procesamos los bordes de la imagen bordes
    self.bordes_imagen_binario = self.bordes_imagen(gris)

    # 3 - Proceso de la imagen, imagen binaria
    self.imagen_binaria = self.imagen_binaria(gris)

    # 4 - Obtenemos el alto, ancho y los canales
    self.alto, self.ancho, self.canal = self.imagen_original.shape

    # 5 - Hacemos una copia
    self.final = self.imagen_original.copy()


  # Utilizamos cv2 para dibujar el rectangulo
  def caja(self, izquierda, derecha, arriba, abajo, color = (255,0,0), tamano = 1):
    # dibujamos el rectangulo en la imagen original
    self.final = cv.rectangle(self.final, (izquierda, arriba), (derecha, abajo), color, tamano)
    return True

  def obtener_imagen_final(self):
    return self.final

  def obtener_imagen_bordes(self):
    return self.bordes_imagen_binario
  
  def obtener_imagen_binario(self):
    return self.imagen_binaria
  
  def obtener_imagen_original(self):
    return self.imagen_original


  def imagen_binaria(self, gray):
    # 1 - Reducir ruido
    blur = cv.GaussianBlur(gray, (3,3), 0)

    # 2 - binarizamos la imagen
    ret, th = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # 3 - reducimos el ruido
    blur2 = cv.GaussianBlur(th, (3,3),0)

    # 4 - Binarizamo la imagen
    ret2, th2 = cv.threshold(blur2, 0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

    return cv.bitwise_not(th2)

  def bordes_imagen(self, gris):
    # 1 - Reducir el ruido con un desenfoque
    blur = cv.GaussianBlur(gris,(3,3),0)

    # 2 - Umbralizar la imagen de forma adaptativa
    thres = cv.adaptiveThreshold(blur,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,5,4) 

    # 3 - Reducimos mas ruido
    blur2 = cv.medianBlur(thres, 3)

    # 4 - Umbralizamos la imagen
    ret3,th3 = cv.threshold(blur2,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

    # 5 - aplicamos un not con CV2, lo que es blanco - negro, negro - blanco.
    return cv.bitwise_not(th3)
