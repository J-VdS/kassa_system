db = "musate_app.db"
zichtbaar_int = ["Nee", "Ja", "Enkel voor kassa"] #0,1,2

expand_size = 15

kassa_cols = 8
kassa_rows = 5

product_cols = 4
product_rows = 5
product_name_max = 26
COLOURS = {}

bewerk_NT = "Bewerken is niet toegelaten.\nJe moet eerst bewerken activeren!"
bewerk_opslaan = "De bewerkte bestelling wordt overschreven!\n\nNaargelang de instelling worden de toegevoegde artikelen naar de printer(s) gestuurd.\nDit kan niet ongedaan worden gemaakt!"
bewerk_start = "Opgepast dit is een gevaarlijke actie en kan niet ongedaan worden gemaakt (nadat je je veranderingen hebt opgeslagen). Druk op opslaan om te bevestigen.\n\n'+' =  item toevoegen, '-' = item verminderen, 'DEL' = verwijder het product van de rekening."

help_connect = "Om een printer toe te voegen moet je het IP adres en de poort van je printer invullen in de daarvoor voorziene tekstvakken. Je moet ook de types selecteren. Zo zal een 'gerecht' worden doorgestuurd naar de keuken, 'drank' naar de bar, ... Om de printer toe te voegen moet je op '+' drukken.\n\n Je kan je printer ook verwijderen via 'X'."
connect_info_type = "help"

printer_file = "printers.data"

knop_verwijder = "U staat op het punt om een rekening te verwijderen. Dit kan niet ongedaan worden gemaakt! Verwijderen is niet hetzelfde als afronden!!!"
knop_afrekenen = "U ben nog aan het bewerken! Druk op herladen om je wijzigingen ongedaan te maken of op opslaan om je wijzigingen te bewaren."

product_min = "Een negatief aantal van een product is niet toegelaten!"
product_del = "Dit product staat niet op de rekening!\n Er is niets verandert."

selectie_beide = "[color=#ff0000]'Alle ID's' en een waarde in Start ID en/of Eind ID is niet toegelaten![/color]"
selectie_nummer = "[color=#ff0000]Start ID en Eind ID moeten 2 positieve getallen zijn![/color]"
selectie_niets = "[color=#ff0000]Vul een start ID en/of Eind ID in. Je kan ook gewoon 'Alle ID's' aanvinken.[/color]"
selectie_neg = "[color=#ff0000]Enkel positieve getallen (0 inbegrepen), vul je niets in kiest men het grootste/kleinste ID[/color]"   

betaal_methodes = ("cash", "bancontact", "QR-code")

save_log_file = "BST.log"