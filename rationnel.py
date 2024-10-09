
def pgcd(u : int , v : int) -> int :
    u, v = abs(u), abs(v)
    while v != 0:
        u, v = v, u % v
    return u

class Rationnel() :
    """
    une classe pour travailler sur les Rationnels ok
    """

    def __init__(self,num : int = 0,denom : int = 1):
        if type(num) != int :
            raise TypeError("num doit etre entier")
        if type(denom) != int :
            raise TypeError("denom doit etre entier")
        if denom == 0 :
            raise ZeroDivisionError()
        self._num = num
        self._denom = denom

    @property
    def num(self) -> int:
        return self._num

    @num.setter
    def num(self,num : int):
        self._num = num

    @property
    def denom(self) -> int:
        return self._denom

    @denom.setter
    def denom(self,denom : int):
        if type(denom) != int :
            raise TypeError("denom doit etre entier")
        if denom == 0 :
            raise ZeroDivisionError()
        self._denom = denom

    def __str__(self) -> str:
        return str(self.num) + "/" + str(self.denom)
    def reduire(self) -> 'Rationnel' :
        p = pgcd(self.num,self.denom)
        return Rationnel(self.num // p,self.denom // p)

    def add(self,r2 : 'Rationnel') -> 'Rationnel':
        nnum = self.num * r2.denom + r2.num * self.denom
        ndenom = self.denom * r2.denom
        return Rationnel(nnum,ndenom).reduire()

    def __add__(self, r2: 'Rationnel') -> 'Rationnel':
        nnum = self.num * r2.denom + r2.num * self.denom
        ndenom = self.denom * r2.denom
        return Rationnel(nnum, ndenom).reduire()



if __name__ == '__main__':
    r1 = Rationnel(24,36)
    r1.num = 12
    r1.denom = 25
    r2 = r1.reduire()
    print(f"{r1} = {r2}")
    print(f"2 * {r1} = {r1.add(r1)}")
    r3 = r1.add(r2)
    print("coucou")
    r3 = r1 + r2
    print(r3)



