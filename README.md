# StreamKitAuto
StreamKitAuto est un outil que j'ai crée sur mesure pour StreamLab ! Il permet de changer dynamiquement l'URL de StreamKit, ainsi si vous changez de vocal, le changement aura également lieu dans StreamLab !

# Explication du soucis
J'ai découvert ce magnifique outil qu'est [StreamKit](https://streamkit.discord.com/overlay) qui permet d'afficher qui est dans votre vocal discord mais sans capturer l'application discord. C'est indépendant d'une quelconque appli !
Donc trop cool nan ?

## LE SOUCIS !
Alors oui, un défaut ! J'ai remarqué que l'URL est fixe ! C'est à dire, que dans l'URL:
``https://streamkit.discord.com/overlay/status/1473349397247950860/11111111121565465...``
Les chiffres sont bien des ID:
- Le premier est le guildId
- Le second est le channelId

Ce qui m'embettait c'est que rien s'actualisait dans StreamLab. Et j'avais la paresse de penser a le changer en pleins live !

## L'idée !
C'était simple, changer dynamiquement les ID, mais... C'est pas si simple !

## Les obstacles
1. Utiliser un bot, classique mais non
Non, il faut en créer un, bref c'est chiant, et quand vous etes en appel privé ou de groupe, ca le détecte pas ! Et dans les serveurs privés ? Encore moins ! Donc non faut trouver autrement !

2. Le self-bot !
Bon... Je veux pas me faire ban, j'ai Nitro, je prends pas le risque !

## ALORS COMMENT ?!
J'ai observé Discord, et j'ai pensé a une option simple, y'a BetterDiscord, qui permet l'injection de code JS, et ca tombe bien, quand on va en vocal, au dessus du bouton de mute, déconexion, y a le nom du channel où on voc, et ceci est une balise <a> contenant une URL, qui n'est autre que... le guildID (id serveur) et channelId (id canal) ! Pile ce qu'il nous faut pour ajuster le lien !

Ok, j'avoue le codage était facile mais pas évident, bref j'y arrive, je filtre les balises qui ont le début de classes ou ID que je cherche bref c'est facile. Maintenant, comment je passe ça a StreamLab ?

Je découvre que StreamLab à un WebSocket... MAIS PTN il est pas documenté et aucun projet qui s'en sert se trouve sur internet ! Mais dieu merci, y'a [Claude](https://claude.ai) que je vous encourage a tester, il m'a tiré d'affaire avec des essais !

Bref je crée un backend en Python, il réceptionne les ID venant de mon plugin via un WebSocket aussi, et après je les envoie à StreamLab ! 

Ca a l'air simple dis comme ca, mais ca m'a pris 3j a développer et penser !

## Schéma logique
Ordre de démarrage:
1. Discord
2. Plugin BetterDiscord
3. Backend Python

Exemple de communication au démarrage:
[BetterDiscord: detection de présence vocal] --- envoi --- > [Backend Python: Réception > Envoie via WebSocket à StreamLab de l'URL] --- envoi --- > [StreamLab: Insértion de l'URL]

# Installation
## Plugin BetterDiscord
1. Installez [BetterDiscord](https://betterdiscord.app/)
2. Allez dans Paramètres > Plugins > Icone Dossier en haut à gauche (Open Plugin Folder)
3. Déposez y ce [fichier]() et activez-le !

> Je terminerai ce document plus tard !
