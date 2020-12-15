import random
import re
import os
import math


def cat():
    categorii = ""
    for name in os.listdir('categorii'):
        categorii = categorii + name + ", "
    categorii = categorii[:-2]
    print("Categoriile existente sunt:", categorii)
    path = "categorii\\"
    categorie = input("Alegeti o categorie: ")
    while not os.path.exists(path + categorie):
        print("Va rugam alegeti una din categoriile existente")
        categorie = input("Alegeti o categorie: ")
    return categorie


def get_cuvant(categorie):
    path = "categorii\\"
    cuvinte = open("%s" % path + categorie).read().splitlines()
    cuvant = random.choice(cuvinte).lower()
    print("Cuvantul de ghicit este: " + re.sub("\w", "*", cuvant))
    return cuvant


def diff(cuv):
    print("Dificultatile disponibile: normal | greu")
    dificultate = input("Alegeti dificultatea: ")
    while dificultate != "normal" and dificultate != "hard":
        dificultate = input("Alegeti dificultatea: ")
    if dificultate == "normal":
        nr_incercari = round(len("".join(set(cuv))) / 2)
        modifier = 1
    else:
        nr_incercari = round(math.log2(len("".join(set(cuv)))))
        modifier = 2
    return nr_incercari, modifier


joc = True
if __name__ == "__main__":
    while joc:
        ghicit = False
        incercari = ""
        pattern = "[^\W]"
        nume = input("Introduceti numele dumneavoastra: ")
        scor = 0
        categorie = cat()
        secret = get_cuvant(categorie)
        incercari_maxime, mod = diff(secret)
        incercari_ramase = incercari_maxime
        print("Mai aveti " + str(incercari_ramase) + " incercari")
        while incercari_ramase > 0 and ghicit is False:
            litera = input("Introduceti o litera: ").lower()
            while litera in incercari or litera.isalpha() is False or len(litera) != 1:
                if litera in incercari:
                    print("Ati mai incercat odata litera asta!")
                else:
                    print("Mai incercati odata!")
                litera = input("Introduceti o litera: ").lower()
            incercari = incercari + litera
            if litera in secret:
                pattern = pattern[:-1]
                pattern += litera + "]"
                print("Felicitari, ati gasit o litera!")
                print("Cuvantul de ghicit este: " + re.sub(r"%s" % pattern, "*", secret))
                scor = scor + 50
                if re.sub(r"%s" % pattern, "*", secret) == secret:
                    scor = (scor + 100) * mod
                    ghicit = True
            else:
                print("Litera aceasta nu exista in cuvant")
                scor = scor - 10
                incercari_ramase -= 1
                print("Mai aveti " + str(incercari_ramase) + " incercari")
        if incercari_ramase == 0:
            print("Ati pierdut! Cuvantul era " + secret)
            print("Incercari esuate: " + str(incercari_maxime))
            print("Scorul dumneavoastra este: " + str(scor))
            f = open("scoruri.txt", "a")
            f.write(str(nume) + "     " + str(scor) + "\n")
            f.close()
        if ghicit:
            print("Ati reusit! Cuvantul era " + secret)
            print("Incercari esuate: " + str(incercari_maxime - incercari_ramase))
            print("Scorul dumneavoastra este: " + str(scor))
            f = open("scoruri.txt", "a")
            f.write(str(nume) + "     " + str(scor) + "\n")
            f.close()
        confirmare = input("Doriti sa mai jucati odata? (da/nu)\n")
        while confirmare != "da" and confirmare != "nu":
            print("Raspundeti cu da sau nu")
            confirmare = input("Doriti sa mai jucati odata? (da/nu)\n")
        if confirmare == "nu":
            joc = False
