from torre import torre

class TorreAmetralladora(torre):
    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            nombre="Torre de Ametralladora",
            costo=25,
            rango=150,
            cadencia_fuego=200, 
            daño=10,
            imagen_torre="imagen"
        )
        
        