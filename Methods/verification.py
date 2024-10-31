


def verification(hod, pozice, Player, array):             #vstupní parametry, padlě číslo, aktuální pozice hráče, aktualni hráč,  hrací plocha
  
    x = hod
    soucet = 0 

    aktualni_pozice = 1

    if (Player.position + hod > 100):                    # pokud aktualní pozice + hod je větší než 100, hod neproběhne
       print('hod neproběhl !!!') 
       aktualni_pozice = pozice

    else:
      
      while x == 6:                                      # pokud padlě číslo je 6, hod se opakuje
        soucet = soucet + 6    
        x = Player.roll_dice()
        print(f'Hráč {Player.name} hodil/a: {x}')

        if (Player.position + soucet + x > 100):         # pokud se jedná o poslední hod a překročí hodnotu 100, hod neproběhne 
            x = 0  
            print('hod neproběhl2 !!!') 
    
      aktualni_pozice = pozice + soucet + x              # nová aktuální pozice
      y = aktualni_pozice

    if (aktualni_pozice < len(array) and array[aktualni_pozice-1].shift != 0):        # výpočet nové pozice, ověření, zda na konkrétním poli hrací plohy není,                                                                                           uplatněno pravidlo např. had, žebřík
        aktualni_pozice = aktualni_pozice + array[aktualni_pozice-1].shift
        zprava = f"Hráč {Player.name} byl/a na pozici {y} a posunul se na pozici {aktualni_pozice}" 
        print(zprava)
         
    return aktualni_pozice                                # vratí se aktuální pozici   