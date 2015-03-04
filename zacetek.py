
class Othello():
    def __init__(self, beli=18, crni=18):
        self.polje = [[0 for x in range(6)] for y in range(6)]
        self.beli = beli
        self.crni = crni
        
    def zacetna_pozicija(self):
        self.polje[2][2] = 1
        self.polje[2][3] = -1
        self.polje[3][2] = 1
        self.polje[3][3] = -1
        return self.polje

    def vstavi_crni_zeton(self, crni, x, y):
        """Vstavi črni žeton zalogo črnih žetonov zmanjša za 1"""
        self.polje[y][x] = -1
        self.crni -= 1

    def vstavi_beli_zeton(self,beli,x,y):
        """Vstavi beli žeton in zalogo belih žetonov zmanjša za 1"""
        self.polje[y][x] = 1
        self.beli -= 1
        
###Tole je za računalnik######################
    def isci_crnega(self):
        for i in range(6):
            x = i%6
            y = i//6
            if self.polje[y][x] != -1:
                pass
            else:
                return (x,y)
##############################################
            
    def preobrni_v_desno(self, x, y):
        """Obrne žetone desno od vstavljenega žetona"""
        barva=self.polje[y][x]
        i=1
        while self.polje[y][x+i] == -barva:
            self.polje[y][x+i] == -self.polje[y][x+i]
            i += 1

    def preobrni_v_levo(self, x, y):
        """Obrne žetone levo od vstavljenega žetona"""
        barva=self.polje[y][x]
        i = 1
        while self.polje[y][x-i] == -barva:
            self.polje[y][x-i] == -self.polje[y][x-i]
            i += 1

    def preobrni_navzdol(self, x, y):
        """Obrne žetone pod vstavljenim žetonom"""
        barva=self.polje[y][x]
        i = 1
        while self.polje[y+i][x] == -barva:
            self.polje[y+i][x] == -self.polje[y+i][x]
            i += 1

    def preobrni_navzgor(self, x, y):
        """Obrne žetone nad vstavljenim žetonom"""
        barva=self.polje[y][x]
        i = 1
        while self.polje[y-i][x] == -barva:
            self.polje[y-i][x] == -self.polje[y-i][x]
            i += 1

    def preobrni_jugovzhod(self, x, y):
        """Obrne žetone po diagonali v smeri desno-dol"""
        barva=self.polje[y][x]
        i = 1
        while self.polje[y+i][x+i] == -barva:
            self.polje[y+i][x+i] == -self.polje[y+i][x+i]
            i += 1

    def preobrni_jugozahod(self, x, y):
        """Obrne žetone po diagonali v smeri levo-dol"""
        barva=self.polje[y][x]
        i = 1
        while self.polje[y+i][x-i] == -barva:
            self.polje[y+i][x-i] == -self.polje[y+i][x-i]
            i += 1

    def preobrni_severovzhod(self, x, y):
        """Obrne žetone po diagonali v smeri desno-gor"""
        barva=self.polje[y][x]
        i = 1
        while self.polje[y-i][x+i] == -barva:
            self.polje[y-i][x+i] == -self.polje[y-i][x+i]
            i += 1

    def preobrni_severozahod(self, x, y):
        """Obrne žetone po diagonali v smeri levo-gor"""
        barva=self.polje[y][x]
        i = 1
        while self.polje[y-i][x-i] == -barva:
            self.polje[y-i][x-i] == -self.polje[y-i][x-i]
            i += 1

    def seznam_sosedov(self, x, y):
        """Vrne seznam sosedov polja s koordinatami (x,y)"""
        p = self.polje
        if x == 0:
            if y == 0:
                return [p[y][x+1], p[y+1][x+1], p[y+1][x]]
            elif y == 5:
                return [p[y][x+1], p[y-1][x+1], p[y-1][x]]
            else:
                return [p[y-1][x], p[y-1][x+1], p[y][x+1], p[y+1][x+1], p[y+1][x]]
        elif x == 5:
            if y == 0:
                return [p[y][x-1], p[y+1][x-1], p[y+1][x]]
            elif y == 5:
                return [p[y][x-1], p[y-1][x-1], p[y-1][x]]
            else:
                return [p[y-1][x], p[y-1][x-1], p[y][x-1], p[y+1][x-1], p[y+1][x]]
        else:
            if y == 0:
                return [p[y][x-1], p[y+1][x+1], p[y+1][x], p[y+1][x+1], p[y][x+1]]
            elif y == 5:
                return [p[y][x-1], p[y-1][x-1], p[y-1][x], p[y-1][x+1], p[y][x+1]]
            else:
                return [p[y][x-1], p[y][x+1], p[y+1][x-1], p[y+1][x], p[y+1][x+1], p[y-1][x-1], p[y-1][x], p[y-1][x+1]]
    

        
            
        

    

