# Kassasysteem via kivy
## Instalatie
Om de kassa te gebruiken heb je momenteel python (> 3.6) nodig. En start server_gui.py. In de tab connecties moet je de server openen via de aan/uit switch. In de laatste versie zal de server sluiten indien er een netwerkerror optreedt. Deze wordt nog niet getoond op het scherm enkel in de terminal!

## Todo's
### algemeen:
 - [ ] verwijder printstatements
 ### client:
 - [ ] meerdere gangen implementatie
 - [x] bestelling aanpassen
 - [ ] netcode herschrijven
 - [x] Vermijd versturen bestelling als de server gesloten is
 - [x] back-ups
 - [ ] (buildozer android release + optimalisatie)
 ### servergui:
 - ~~[ ] settings~~
 - [x] ticketprinter bij kassa
 - [x] statistieken
 - [ ] oplossingen meerdere jaren --> database herschrijven
 - [x] aanpassen rekening
 - [x] visuele aanpassing
	 - [x] kleur in label
	 - [x] popups 
- [ ] popups wanneer de server sluit
- [ ] popups wannneer errors
 ### printserver:
 - [x] ticket uitprinten en verwerken
 - [ ] papier op controle + inwendige printer storage controle
 - [x] nagaan correct afsluiten!
 - [ ] herschrijven netcode
 - [ ] ( geluid uit )
 
 ### stress test:
 - [x] voeg een time.sleep toe aan printserver bij het verwerken van een bericht. Sluit de connectie via de server_gui, normaal zou de printer blijven printen.

Indien er problemen of vragen zijn, vermeldt deze dan in de Issues tab van github.com .
 

> Written with [StackEdit](https://stackedit.io/).
