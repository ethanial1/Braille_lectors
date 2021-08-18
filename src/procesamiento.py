import cv2 as cv
from math import sqrt
from collections import Counter
from .braille import Braille

class Procesamiento(object):
  def __init__(self, image):
    self.image = image
    self.iniciar = False
    self.puntos = []
    self.diametro = 0.0
    self.radio = 0.0
    self.next_epoch = 0
    self.letras = []

  
  # Iterable
  def __iter__(self):
    return self
  
  def __next__(self):
    return self.siguiente()
  
  def siguiente(self):
    # 1 - 
    if not self.iniciar:
      self.iniciar = True

      # 1 - Obtener los contornos de la imagen
      contornos = self.procesar_contornos_imagen()

      if len(contornos) == 0:
        self.limpiar()
        raise StopIteration() # Detenemos la iteración.
      
      # 2 - Buscamos los circulos en la imagen
      circulos_rodean = self.obtener_circulos_rodean(contornos)
      if len(circulos_rodean) == 0:
        self.limpiar()
        raise StopIteration() # Detenemos la iteración.
      
      # 3 - Obtenemos el diametro, los puntos y radio no repetidos
      diametro, puntos, radio = self.obtener_puntos_validos(circulos_rodean)
      if len(puntos) == 0:
        self.limpiar()
        raise StopIteration() # Detenemos la iteración.
      
      # 4 - Asignamos los valores
      self.diametro = diametro
      self.puntos = puntos
      self.radio = radio
      self.next_epoch = 0
      self.letras = []

    
    # 2 - Evaluamos si existen letras en el arreglo
    if len(self.letras) > 0:
      r = self.letras[0]
      # eliminamos
      del self.letras[0]
      return r
    
    # 3 - obtenemos las coordenadas de las filas, filas rectas, hasta donde llega
    fila = self.obtener_fila(self.puntos, self.next_epoch)
    if fila is None:
      self.limpiar()
      raise StopIteration() # Detenemos la iteración.

    # 4 - coordenada en y
    arriba = int(fila[1] - int(self.radio * 1.5))
    self.next_epoch = int(fila[1] + self.radio)

    #
    fila = self.obtener_fila(self.puntos, self.next_epoch, self.diametro, True)
    if fila is None:
      self.next_epoch = int(self.next_epoch + (2 * self.diametro))
    else:
      self.next_epoch = int(fila[1] + self.radio)
    
    fila = self.obtener_fila(self.puntos, self.next_epoch, self.diametro, True)
    if fila is None:
      self.next_epoch = int(self.next_epoch + (2 * self.diametro))
    else:
      self.next_epoch = int(fila[1] + self.radio)
    

    # 5 - 
    abajo = self.next_epoch
    self.next_epoch += int(2*self.diametro)


    # 6 - Obtenemos los puntos de una region
    d_puntos = self.obtener_puntos_region(self.puntos, arriba,abajo)
    siguiente = 0

    while True:
      # Obtenemos las columnas de la region
      xcoor = self.obtener_columna(d_puntos, siguiente)
      if xcoor is None:
        break
      
      izquierda = int(xcoor[0] - self.radio) # coordenada x
      siguiente = int(xcoor[0] + self.radio)
      xcoor = self.obtener_columna(d_puntos,siguiente, self.diametro, True)

      if xcoor is None:
        siguiente += int(self.diametro * 1.5)
      else:
        siguiente = int(xcoor[0]) + int(self.radio)
      
      derecha = siguiente
      caja = (izquierda, derecha, arriba, abajo)
      # Obtenemos los puntos que estan en la caja
      dts = self.obtener_puntos_caja(d_puntos, caja)

      char = Braille(dts, self.diametro, self.radio, self.image)
      char.izquierda = izquierda
      char.derecha = derecha
      char.arriba = arriba
      char.abajo = abajo
      
      #char = (dts, self.diametro, self.radio, izquierda, derecha, arriba, abajo)
      #print(char)
      self.letras.append(char)

    if len(self.letras) < 1:
      self.limpiar()
      raise StopIteration() # Detenemos la iteración.
    
    r = self.letras[0]
    del self.letras[0]

    return r

    
  # Obtener los puntos en base a cordenadas que forman una caja
  def obtener_puntos_caja(self, puntos, caja):
    izquierda, derecha, arriba, abajo = caja
    resultado = []

    for punto in puntos:
      x,y = punto[0]
      if x >= izquierda and x <= derecha and y >= arriba and y <= abajo:
        resultado.append(punto)
    
    return resultado

  # Obtener los puntos de una region
  def obtener_puntos_region(self, puntos, y1, y2):
    d = []
    if y2 < y1:
      return d
    
    for punto in puntos:
      x,y = punto[0]
      if y > y1 and y < y2:
        d.append(punto)
    
    return d
  
  # Obtenemos las columnas
  def obtener_columna(self, puntos, epoca = 0, diametro = 0, salto = False):
    if len(puntos) == 0:
      return None
    
    minPunto = None

    for punto in puntos:
      x,y = punto[0]
      if x < epoca:
        continue
      
      if minPunto is None:
        minPunto = punto
      else:
        v = int(x - epoca)
        minv = int(minPunto[0][0] - epoca)
        if minv > v:
          minPunto = punto
        else:
          continue
    if minPunto is None:
      return None

    if salto:
      v = int(minPunto[0][0] - epoca)
      if v > (2 * diametro):
        return None # Indica que no se ha fijado toda la fila
      
    return minPunto[0] # (x,y)

  # Obtenemos las filas
  def obtener_fila(self, puntos, epoca = 0, diametro = 0, salto = False):
    if len(puntos) == 0:
      return None
    
    minPunto = None

    for punto in puntos:
      x,y = punto[0]
      if y < epoca:
        continue
      
      if minPunto is None:
        minPunto = punto
      else:
        v = int(y - epoca)
        minv = int(minPunto[0][1] - epoca)
        if minv > v:
          minPunto = punto
        else:
          continue
    if minPunto is None:
      return None
    
    if salto:
      v = int(minPunto[0][1] - epoca)
      if v > (2 * diametro):
        return None # Indica que no se ha fijado toda la fila
      
    return minPunto[0] # (x,y)
      
    
  # Obtenemos los puntos validos en la imagen
  def obtener_puntos_validos(self, circulos):
    tolerancia = 0.45
    radiio = []
    consider = []
    bin_imagen = self.image.obtener_imagen_binario()

    for circulo in circulos:
      x,y = circulo[0]
      rad = circulo[1]

      it = 0
      while it < int(rad):
        if bin_imagen[y,x+it] > 0 and bin_imagen[y+it,x] > 0:
          it += 1
        else:
          break
      else:
        if bin_imagen[y,x] > 0:
          consider.append(circulo)
          radiio.append(rad)
    
    prueba = Counter(radiio).most_common(1)[0][0]
    puntos = []

    for circulo in consider:
      x,y = circulo[0]
      rad = circulo[1]

      # Evaluamos si es menor o igual
      if rad <= int(prueba * (1 + tolerancia)) and rad >= int(prueba * (1 - tolerancia)):
        puntos.append(circulo)
    
    # Pueden existir circulos duplicados, los eliminamos
    
    for punto in puntos:
      x,y = punto[0]
      c1 = punto[1]
      for spunto in puntos:
        if punto == spunto:
          continue
        x2,y2 = spunto[0]
        c2 = spunto[1]
        d = sqrt((x2 - x) **2) + ((y2-y)**2)
        if c1 > (d + c2):
          puntos.remove(spunto)
    

    # Radio
    radiio = []
    for punto in puntos:
      radio = punto[1]
      radiio.append(radio)
    
    prueba = Counter(radiio).most_common(1)[0][0]

    return 2*(prueba), puntos, prueba

  
  def obtener_circulos_rodean(self, contornos):
    # Localizamos todos los circulos y obtenemos sus coordenadas y el radio
    circulos = []
    for contorno in contornos:
      (x,y), radio = cv2.minEnclosingCircle(contorno)
      centro = (int(x), int(y))
      radio = int(radio)
      circulos.append((centro, radio))
    

    return circulos
  

  def limpiar(self):
    self.image = None
    self.iniciar = False
    self.puntos = []
    self.diametro = 0.0
    self.radio = 0.0
    self.next_epoch = 0.0
    self.letras = []
  
  def procesar_contornos_imagen(self):
    # Obtener la imagen binaria
    imagen_bordes = self.image.obtener_imagen_bordes()

    # Buscar los contornos
    contornos = cv.findContours(imagen_bordes, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    if len(contornos) == 2:
      contornos = contornos[0]
    else:
      contornos = contornos[1]
    
    return contornos
  
