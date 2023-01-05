

## Roadmap

1. caricamento spritesheet per il player
2. caricamento di un singolo sprite dallo spritesheet
3. creazione della classe Player(pg.sprite.Sprite) e rappresentazione a schermo
4. fix del clock a 60 fps
5. movimento dello sprite
6. input utente per muovere lo sprite (ASWD) 4 direzioni
7. movimento nelle 8 direzioni
8. fix movimento diagonale e inserimento vettore float per le posizioni
9. refactor della classe player + spritesheet class (primo passo)
10. generalizziamo Spritesheet.get_player_surface(self) -> Spritesheet.get_surface(self,row,col,size=..., scale  = ...)
11. possibilità di definire degli sprite per nome e recuperare i riferimenti alla surface relativa (Spritesheet.py)
12. configurazione dello spritesheet da file json
13. creazione e caricamento di una mappa da file di testo
14. importazione di una mappa da tiled
15. pygame groups & camera
16. velocita del player 
17. posizionare il player sulla mappa

### todo

- [x] spritesheet refactor ( Spritesheet e WorldSpritesheet sono la stessa classe in fondo)
- [x] remove  `get_player_surface()`. animazioni negli spritesheet
- [x] sprite per il movimento del player, solo direzione
- [x] walk animation per il player e movimento aggiornato
- [x] collisioni con la mappa (rimozione movimento diagonale)
- [x] display arma per il player
- [ ] creazione azione di attacco e gestione timer nel player
- [ ] attacco nella direzione in cui sto guardando

## credits

pixel mood assets: https://alwore.itch.io/pixel-mood