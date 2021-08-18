class Symbol(object):
    def __init__(self, value = None, letter = False, special = False):
        self.is_letter = letter
        self.is_special = special
        self.value = value

    def is_valid(self):
        r = True
        r = r and (self.value is not None)
        r = r and (self.is_letter is not None or self.is_special is not None)
        return r

    def letter(self):
        return self.is_letter

    def special(self):
        return self.is_special


class clasificadorBraille(object):
  # Letras del alfabeto
  '''
  simbolos = {
      (1,0,0,0,0,0): 'a',
      (1,1,0,0,0,0): 'b',
      (1,0,0,1,0,0): 'c',
      (1,0,0,1,1,0): 'd',
      (1,0,0,0,1,0): 'e',
      (1,1,0,1,0,0): 'f',
      (1,1,0,1,1,0): 'g',
      (1,1,0,0,1,0): 'h',
      (0,1,0,1,0,0): 'i',
      (0,1,0,1,1,0): 'j',
      (1,0,1,0,0,0): 'k',
      (1,1,1,0,0,0): 'l',
      (1,0,1,1,0,0): 'm',
      (1,0,1,1,1,0): 'n',
      (1,0,1,0,1,0): 'o',
      (1,1,1,1,0,0): 'p',
      (1,1,1,1,1,0): 'q',
      (1,1,1,0,1,0): 'r',
      (0,1,1,1,0,0): 's',
      (0,1,1,1,1,0): 't',
      (1,0,1,0,0,1): 'u',
      (1,1,1,0,0,1): 'v',
      (0,1,0,1,1,1): 'w',
      (1,0,1,1,0,1): 'x',
      (1,0,1,1,1,1): 'y',
      (1,0,1,0,1,1): 'z',
      (0,0,1,1,1,1): '#',
  }
  '''
  simbolos = {
         (1,0,0,0,0,0): Symbol('a',letter=True),
         (1,1,0,0,0,0): Symbol('b',letter=True),
         (1,0,0,1,0,0): Symbol('c',letter=True),
         (1,0,0,1,1,0): Symbol('d',letter=True),
         (1,0,0,0,1,0): Symbol('e',letter=True),
         (1,1,0,1,0,0): Symbol('f',letter=True),
         (1,1,0,1,1,0): Symbol('g',letter=True),
         (1,1,0,0,1,0): Symbol('h',letter=True),
         (0,1,0,1,0,0): Symbol('i',letter=True),
         (0,1,0,1,1,0): Symbol('j',letter=True),
         (1,0,1,0,0,0): Symbol('K',letter=True),
         (1,1,1,0,0,0): Symbol('l',letter=True),
         (1,0,1,1,0,0): Symbol('m',letter=True),
         (1,0,1,1,1,0): Symbol('n',letter=True),
         (1,0,1,0,1,0): Symbol('o',letter=True),
         (1,1,1,1,0,0): Symbol('p',letter=True),
         (1,1,1,1,1,0): Symbol('q',letter=True),
         (1,1,1,0,1,0): Symbol('r',letter=True),
         (0,1,1,1,0,0): Symbol('s',letter=True),
         (0,1,1,1,1,0): Symbol('t',letter=True),
         (1,0,1,0,0,1): Symbol('u',letter=True),
         (1,1,1,0,0,1): Symbol('v',letter=True),
         (0,1,0,1,1,1): Symbol('w',letter=True),
         (1,0,1,1,0,1): Symbol('x',letter=True),
         (1,0,1,1,1,1): Symbol('y',letter=True),
         (1,0,1,0,1,1): Symbol('z',letter=True),
         (0,0,1,1,1,1): Symbol('#',special=True),
    }

  def __init__(self):
    self.resultado = ''
    self.on = False
    self.ends = None
    self.number = False
    return

  # Le pasamos la tupla que tiene las coordenadas de todos los 
  # puntos y la caja
  def push(self, letra):
    if not letra.is_valid():
      return
    
    caja = letra.get_caja()
    puntos = letra.get_punto_coordenadas()
    diametro = letra.get_punto_diametro()
    end, start, width, combinacionP = combinacion(caja, puntos, diametro)

    if combinacionP not in self.simbolos:
      self.resultado += '?'
      return

    if self.ends is not None:
      dist = obtener_distancia(self.ends, start)
      if dist * 0.5 > (width**2):
        self.resultado += " "
    self.ends = end

    simbol = self.simbolos[combinacionP]
    if simbol.letter() and self.number:
      self.number = False
      self.resultado += translate_to_number(simbol.value)
    elif simbol.letter():
      if self.on:
        self.resultado += simbol.value.upper()
      else:
        self.resultado += simbol.value
    else:
      if simbol.value == '#':
        self.number = True

    return 
  
  def obtener_resultado(self):
    return self.resultado
  

  # Método que nos ayuda a saber la combinación y por lo tanto la letra
def combinacion(caja, puntos, diametro):
    result = [0,0,0,0,0,0]
    izquierda, derecha, arriba, abajo = caja

    midpointY = int((abajo - arriba)/2)
    end = (derecha, midpointY)
    start = (izquierda, midpointY)
    width = int(derecha - izquierda)

    # 1 4
    # 2 5
    # 3 6
    esquinas = {
        (izquierda,arriba): 1,     
        (derecha, arriba): 4,
        (izquierda, abajo): 3, 
        (derecha, abajo): 6,
        (izquierda): 2,
        (derecha) : 5,
        }
    
    for esquina in esquinas:
      if esquina != izquierda and esquina != derecha:
        d = obtener_puntos_cercanos(puntos, int(diametro), esquina)
      else:
        if esquina == izquierda:
          d = obtener_izquierda_cerca(puntos, int(diametro), izquierda)
        else:
          d = obtener_derecha_cerca(puntos, int(diametro), derecha)
      
      if d is not None:
        puntos.remove(d)
        result[esquinas[esquina] -1] = 1
      
      if len(puntos) == 0:
        break
    
    return end, start, width, tuple(result)

  

def obtener_izquierda_cerca(puntos, diametro, izquierda):
    cerca = None
    for punto in puntos:
      x,y = punto[0]
      dist = int(x - izquierda)

      if dist <= diametro:
        if cerca is None:
          cerca = punto
        else:
          x1,y1 = cerca[0]
          dist2 = int(x1-izquierda)
          if dist2 > dist:
            cerca = punto
    
    return cerca

def obtener_derecha_cerca(puntos, diametro, derecha):
    cerca = None
    for punto in puntos:
      x,y = punto[0]
      dist = int(derecha - x)

      if dist <= diametro:
        if cerca is None:
          cerca = punto
        else:
          x1,y1 = cerca[0]
          dist2 = int(derecha - x1)
          if dist2 > dist:
            cerca = punto
    
    return cerca

def obtener_puntos_cercanos(puntos, diametro, pt1):
    cerca = None
    diametro **=2
    for punto in puntos:
      pin = punto[0]
      distancia = obtener_distancia(pin, pt1)

      if distancia <= diametro:
        if cerca is None:
          cerca = punto
        else:
          pt = cerca[0]
          ndistancia = obtener_distancia(pt, pt1)
          if ndistancia >= distancia:
            cerca = punto
    
    return cerca
  
  # Obtenemos la distancia entre los puntos
def obtener_distancia(p1,p2):
    x1,y1 = p1
    x2,y2 = p2

    return ((x2 - x1) **2) + ((y2 - y1)**2)

  
def translate_to_number(value):
    if value == 'a':
        return '1'
    elif value == 'b':
        return '2'
    elif value == 'c':
        return '3'
    elif value == 'd':
        return '4'
    elif value == 'e':
        return '5'
    elif value == 'f':
        return '6'
    elif value == 'g':
        return '7'
    elif value == 'h':
        return '8'
    elif value == 'i':
        return '9'
    else:
        return '0'




