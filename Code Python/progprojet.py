## Programme python du projet plante connectée


import requests
import json


            ## Connexion à l'API :

print("**********************************************")   
print("\n        Application plante connectée\n")

url_api = "https://api.thinger.io/"
parametre = "oauth/token"

main_api = url_api+parametre


username = input("Nom d'utilisateur : ")
motdepasse = input("Mot de passe : ")

mydata = {
    "Content-Type":"application/x-www-form-urlencoded",
    "grant_type":"password",
    "username": username,
    "password": motdepasse
    }



        ## interogation de l'api
        
objet_api = requests.post(main_api, data=mydata)
jsondata = objet_api.json()
errorcode = objet_api.status_code


while (errorcode != 200):
    print("erreur ", errorcode)
    print("Une erreur s'est produite, identifiant ou mot de passe incorrect.")
    username = input("Nom d'utilisateur : ")
    motdepasse = input("Mot de passe : ")
    
    mydata["username"] = username
    mydata["password"] = motdepasse
    
    
    objet_api = requests.post(main_api, data=mydata)
    jsondata = objet_api.json()
    errorcode = objet_api.status_code



## print(jsondata)
## print("")

token = jsondata["access_token"]


parametre = "v1/users/" + username + "/devices?authorization=" + token
main_api = url_api+parametre


devices = requests.get(main_api).json()
print("\nListe des équipements (device) :")
for device in devices:
    print(device["device"])

choixdevice = input("Quel équipement voulez vous utiliser ? :")
print("")

## print(devices)
## print("")
print("Connexion en cours...")

onpeutcontinuer = 0 
for device in devices:
    if(choixdevice == device["device"]):
        print(device["device"]," :", end ='' )
        connectionstatus = device["connection"]
        if (connectionstatus["active"] == False):
            print("non connecté")
        else:
            print("connecté")
            onpeutcontinuer = 1
      
           
if (onpeutcontinuer == 1):
    
            ## Récupération depuis Thinger.io
    
    ressource_map = ["luminosity","temperature","humidity","moisture",] 
    
    
    valeurs = []
    for ressource in ressource_map:
        
        parametre = "v2/users/" + username + "/devices/" + choixdevice + "/" + ressource + "?authorization="+ token
        main_api = url_api+parametre
        stats = requests.get(main_api).json()
        ## print(stats)
        if "out" in stats:
            valeurs.append(stats["out"])
        
        ##stats correspond à :  {'out': 24}
        
   
    ## print(valeurs)
    
    
            ## Récupération depuis la base de données :

    plante = "a"
    base = [[0,0],[0,0]]
    
    separateur = ";"
    
    def readfilesep(nom, separateur):
        base = []
        fichier = open(nom, 'r')
        for line in fichier: 
            petit_tab = []
            petit_tab = line.replace('\n','').split(separateur)
            base.append(petit_tab)
            
        fichier.close()
        return base
    
    Donnees = readfilesep("BDD.txt", separateur)
    ## print(Donnees)
    
    
            ## Traitement des données :
    
    plante = input("Quelle est votre plante ? \n")
    
    for entree in Donnees:
        if (plante == entree[0]):
            print ("\nInformations sur : ", entree[0]) 
            print ("L'humidité de l'air idéale est ", entree[3],"%")
            print ("L'humidité du sol idéale est ", entree[4])
            print ("La température idéale est ", entree[2],"degrés")
            print ("La luminosité idéale est ", entree[1],"Lux")
            print ("\n")
            print ("Données actuelles de votre plante") 
            print ("L'humidité de l'air actuelle est ", valeurs[2],"%")
            print ("L'humidité du sol actuelle est ", valeurs[3])
            print ("La température actuelle est ", valeurs[1],"degrés")
            print ("La luminosité actuelle est ", valeurs[0],"Lux")
            
            
            ## Informations suppémentaires:
    
    veplus = input("Voulez vous des informations complémentaires ? (oui ou non) \n")
    
    if (veplus == "oui"):
        
        infossup = readfilesep("InfosPlantes.txt", separateur)
        
        for nom, categorie, info, date in infossup:
            if (plante == nom):
                print ("Informations supplémentaires sur le ", nom) 
                print ("Elle fait partie du groupe des ", categorie)
                print (info, ".") 
                print ("Elle fleurit ", date) 
        
        
        
print ("\n  Merci d'avoir utiliser notre application ")        

