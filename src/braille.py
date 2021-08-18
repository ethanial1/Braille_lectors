# Braille
class Braille(object):
  def __init__(self, coordenadas_punto, diametro, radio, imagen):
    self.izquierda = None
    self.derecha = None
    self.arriba = None
    self.abajo = None
    self.coordenadas_punto = coordenadas_punto
    self.diametro = diametro
    self.radio = radio
    self.imagen = imagen
    return;
  
  # Accedemos a la imagen y 
  def cuadro(self):
    self.imagen.caja(self.izquierda, self.derecha, self.arriba, self.abajo)
  
  def get_imagen(self):
    return self.imagen
  
  def get_punto_diametro(self):
    return self.diametro
  
  def get_punto_radio(self):
    return self.radio
  
  def get_punto_coordenadas(self):
    return self.coordenadas_punto
  
  def get_izquierda(self):
    return self.izquierda
  
  def get_derecha(self):
    return self.derecha
  
  def get_abajo(self):
    return self.abajo
  
  def get_arriba(self):
    return self.arriba
  
  def get_opencv_izquierda_arriba(self):
    return (self.izquierda, self.arriba)
  
  def get_opencv_derecha_abajo(self):
    return (self.derecha, self.abajo)
  
  def get_caja(self, form = "izquierda,derecha,arriba,abajo"):
    r = []
    form = form.split(',')
    if len(form) < 4:
      return (self.izquierda, self.derecha, self.arriba, self.abajo)

    for direction in form:
      direction = direction.lower()
      if direction == 'izquierda':
        r.append(self.izquierda)
      elif direction == 'derecha':
          r.append(self.derecha)
      elif direction == 'arriba':
          r.append(self.arriba)
      elif direction == 'abajo':
          r.append(self.abajo)
      else:
        return (self.izquierda, self.derecha, self.arriba, self.abajo)
        
    return tuple(r)

  def is_valid(self):
    r = True
    r = r and (self.izquierda is not None)
    r = r and (self.derecha is not None)
    r = r and (self.arriba is not None)
    r = r and (self.abajo is not None)
    return r