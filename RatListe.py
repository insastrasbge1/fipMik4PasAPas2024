"""
travail sur les rationnels : représentés par des listes de deux entiers
l[0] --> numérateur
l[1] --> dénominateur
"""
def pgcd(u : int , v : int) -> int :
    u, v = abs(u), abs(v)
    while v != 0:
        u, v = v, u % v
    return u

def reduire(r : list[int]) -> list[int] :
    p = pgcd(r[0],r[1])
    res = [ r[0]//p , r[1]//p ]
    return res

def add(r1 : list[int] , r2 : list[int]) -> list[int] :
    a = r1[0]
    num = a*r2[1] + r2[0]*r1[1]
    denom = r1[1]*r2[1]
    return reduire([ num , denom])

def aff(r : list[int]) -> str :
    return str(r[0]) + "/" + str(r[1])

if __name__ == '__main__':
    test = [24,36]
    testReduit = reduire(test)
    print(f"{aff(test)} -reduit-> {aff(testReduit)}")
    r1 = [1,3]
    print(f"2 r1 : {aff(add(r1,r1))}")
