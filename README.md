# IUTbotEDT
Repo du système distribuant les EDT sur le serveur du BDE Informatique de l'IUT d'Amiens


# Fonctionnement

- Je reçois les EDT par mail comme tout le monde.
- Chaque mail contenant un EDT est redirigé vers une boite GMAIL.
### EdtScrapper.py
-  Avec un script, je regarde toute les X secondes si j'ai un nouveau mail avec un EDT. Si oui, je le download dans un répertoire. "EdtScrapper.py"
### PdfSorter.py
- Est ensuite appelé le script chargé de convertir le PDF en image et faire tout un tas de traitements. Le résultat de ce script se trouve dans le répertoire "EDT".
### BotDiscordEDT.py
- Et finalement, un script chargé de gérer le bot discord, qui quand il reçoit une demande d'emploi du temps, a juste à envoyer une image.
