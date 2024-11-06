def pgcd(u : int , v : int) -> int :
    u, v = abs(u), abs(v)
    while v != 0:
        u, v = v, u % v
    return u

def chose(s1 : str , s2 : str , separateur : str = "/") -> str :
    return s1 + separateur + s2

if __name__ == '__main__':
    """truc = int(input("un entier :"))
    v = int(input("un autre entier :"))
    p = pgcd(truc,v)
    print(f"pgcd = {p}")"""
    print(chose("3","4"))
    print(chose(s2="5",s1="8"))
    print(chose("3","4","//"))
    print(chose("3","4",separateur = "//"))
    print(chose(s2="5",s1="8",separateur="%%"))
    print("cou")
    print("cou")
    print("cou",end=".")
    print("cou")
    print("cou",end="")
    print("cou")

