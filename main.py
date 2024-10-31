## muj prvni program

from Classes.player import Player
from Methods.verification import verification
from Classes.square import Square
from Methods.check import check
from Data.Chessboard import pole2

from termcolor import colored, cprint

import sys
sys.setrecursionlimit(2000) 

# Zadaní počtu hráčů

while True:
    try:
        pocet = int(input("Zadejte počet hráčů [MAX. 10]: "))
        if pocet > 0 and pocet <11:  # kontrola, zda je počet kladné číslo
            break  # ukončí smyčku, pokud je vstup platný
        else:
            print("Počet hráčů musí být kladné číslo! a maximální množství hráčů je 10 !!!")
            print()
    except ValueError:
        print("Chyba: Musíte zadat platné číslo!")
        print()

pole = [] 
## pole2 = []

print()

# Zadaní jednotlivých jmen hráčů

for i in range(pocet):  

    while True:
        try:
            zprava = f"Zadejte jméno {i+1}. hráče: " 
            jmeno = input(zprava)    
            #pole.append(Player(jmeno, 1))
            print()

            if jmeno != '':
                pole.append(Player(jmeno, 1))
                break
            else:
                print("Zadejte prosím slovo!")
                print()
               
 
        except ValueError:
            print("Chyba: Zadejte prosím jméno")
            print()


# Proměnná, za účelem kontroly konce hry

konec = 1

# Proměnná, počet iterací smyčky while
j = 0

while  konec != 100: 
    j = j + 1
    kolo = f"{j}. kolo"
    print()
    print(kolo)
    print("---------")
    print()

    for i in range(pocet): 

        hod = pole[i].roll_dice()                                              # hod kostkou
        zprava = f"Hráč {pole[i].name} hodil/a: {hod}" 
        print(zprava)
        a_position = verification(hod, pole[i].position, pole[i], pole2)       # nová aktuální pozice hráce
        zprava = f"Aktualní pozice hráče {pole[i].name} je: {a_position}"       
        pole[i].position = a_position                                          # přiřazení nové pozice hráči 
        konec = a_position                                                     # kontrola konce hry    
        print(zprava)
        print()    
        check(pole, pole2, pole[i])                                            # kontrola, zda hráč přechází na další místo
     
        if (konec == 100):                                                     # kontrola konce hry
            print()
            cprint(f"Hráč {pole[i].name} vyhrál!!!", 'red', attrs=['blink'])
            print()
            break
        

  
      

        




