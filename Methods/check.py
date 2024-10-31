
from Methods.verification import verification


def check(players, chessboard, Player):                       # vstupní parametry, pole hráčů, hrací plocha, aktuální hráč                    
     
    result = True
    
    while result == True:
        
        for i in range(len(players)):                         # Kontrola, zda při pohybu hráče na další pole, není na tomto poli další hráč
            if (players[i].position == Player.position and players[i].name != Player.name and Player.position > 1):
                 print(f"Hráč {players[i].name} je na stejné pozici jako hráč {Player.name}") 
                 result = True
                 x = players[i].position
                 players[i].position = players[i].position -1 
                 print(f"Hráč {players[i].name} změnil/a pozici z {x} na {players[i].position}")
                 print() 
                                               
                 x = verification(0,players[i].position, players[i], chessboard)   # výpočet nové pozice
                 
                 players[i].position = x

                 ###print(f'Rekurze cislo. {i}')
                 check(players, chessboard, players[i])                            # nová kontrola, zda není na nové pozici, další hráč

            else:

                if players[i].position -1 < 1:                                    # pokud se hráč posune z pozice 1 zpět, vždy bude pozice nastavena na pozici 1
                    players[i].position = 1
                    result = False 
                    break 
         
                result = False
    
    