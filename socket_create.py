import socket 

MaSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Host = '127.0.0.1' # l'ip locale de l'ordinateur
Port = 234         # choix d'un port
 
# on bind notre socket :
MaSocket.bind((Host,Port))
 
# On est a l'ecoute d'une seule et unique connexion :
MaSocket.listen(1)
 
# Le script se stoppe ici jusqu'a ce qu'il y ait connexion :
client, adresse = MaSocket.accept() # accepte les connexions de l'exterieur
print("L'adresse",adresse,"vient de se connecter au serveur !")
while 1:
        RequeteDuClient = client.recv(255) # on recoit 255 caracteres grand max
        if not RequeteDuClient: # si on ne recoit plus rien
                break  # on break la boucle (sinon les bips vont se repeter)
        print(RequeteDuClient,"\a")       # affiche les donnees envoyees, suivi d'un bip sonore