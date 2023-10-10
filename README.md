# iptable_automation

Automatisation du paramétrage du filtrage par des iptables sur un serveur LINUX depuis un client écrit en Python

1. **Prérequis**

Il faut obligatoire exécuter ce script python sur un système Linux.

Il faut la configuration d'un utilisateur (sudoers) qui a le droit d'exécuter le binaire /sbin/iptables sans la commande sudo (Voir la configuration suivante)

Il faut s'assurer le service SSH est activé sur la machine distante (serveur): ``sudo systemctl status ssh`` sinon l'activer via ``sudo apt install -y openssh-server``

2. **Configuration utilisateur sudoers**

Editer le fichiers /etc/sudoers via:

``su - ``

``visudo``

Puis ajouter ``<user_name> ALL=(ALL) NOPASSWD: /sbin/iptables`` après la ligne de #Allow members of group sudo to execute any command.

3. **Exécuter le script**

Avant tout, il faut installer les dépendances du projet via ``./installer.py``

Modifier les règles de filtrage iptables dans le fichier ``iptables_rules.txt``

Modifier les paramètre de connexion SSH:

``server_ip_address, ssh_username et ssh_password ``

Puis lancer le script ``python3 client.py``

4. **Logs**

* Les logs client sont stockés dans le ficher ``client.log``
* Les logs serveur sont stockés dans le fichier /home/<user_name>/iptables.log
