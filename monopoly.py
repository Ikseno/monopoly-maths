import numpy as np

state = {
    1 : ["Départ"],
    2 : ["Bd de Belleville"],
    3 : ["Caisse Communauté 3"],
    4 : ["Rue Lecourbe"],
    5 : ["Impôts sur le revenu"],
    6 : ["Gare Montparnasse"],
    7 : ["Rue Vaugirard"],
    8 : ["Chance 8"],
    9 : ["Rue de Courcelles"],
    10 : ["Av de la République"],
    11 : ["Prison"],
    12 : ["Bd de la Villette"],
    13 : ["Compagnie distribution electricité"],
    14 : ["Av de Neuilly"],
    15 : ["Rue du Paradis"],
    16 : ["Gare de Lyon"],
    17 : ["Avenue Mozart"],
    18 : ["Caisse Communauté 18"],
    19 : ["Bd Saint Michel"],
    20 : ["Place Pigale"],
    21 : ["Parc Gratuit"],
    22 : ["Av Matignon"],
    23 : ["Chance 23"],
    24 : ["Bd Malesherbes"],
    25 : ["Av Henri Martin"],
    26 : ["Gare du Nord"],
    27 : ["Fbg Saint Honoré"],
    28 : ["Place de la Bourse"],
    29 : ["Cie de distribution des eaux"],
    30 : ["Rue La Fayette"],
    31 : ["Allez en prison"],
    32 : ["Av de Breteuil"],
    33 : ["Avenue Foch"],
    34 : ["Caisse Communauté 34"],
    35 : ["Bd des Capucines"],
    36 : ["Gare Saint Lazare"],
    37 : ["Chance 37"],
    38 : ["Champs Elysées"],
    39 : ["Taxe de Luxe"],
    40 : ["Rue de la Paix"]
}


'''Voici la liste détaillée des cartes ''Chance'' : 1 envoie en prison, 1 envoie vers l’avenue Henri-
Martin, 1 envoie vers boulevard de la Villette, 1 envoie vers la Rue de la Paix, 1 envoie vers la gare
de Lyon, 1 envoie sur la case Départ, 1 ''Reculez de trois cases''. Il y a 9 autres cartes ''Chance'' qui
n’ont aucune influence sur la position
Voici maintenant la liste détaillée des cartes ''Caisse de Communauté'' : 1 ''Retournez à Belleville'',
1 envoie en prison, 1 envoie sur la case Départ, 1 possibilité de tirer une carte ''Chance'' (alternative
avec une amende). Il y a 12 autres cartes ''Caisse de Communauté'' qui n’ont aucune influence sur la
position'''

carte_chance_possibilite = [11-1,25-1,12-1,40-1,16-1,1-1] # l'ensemble des cases surlesquelles on peut aller en tirant une carte chance (sauf reculer de 3 cases)

carte_communaute_possibilite = [2-1,11-1,1-1] # on paye une amende (donc pas carte chance)


# CREATION DE LA MATRICE D'ADJACENCE


array = []

probas_2_de = [1/36,2/36,3/36,4/36,5/36,6/36,5/36,4/36,3/36,2/36,1/36] # probabilité pour la somme de deux dés (premier element correspond à une somme valant 2, dernier valant 12)

for j in range(40): # creation d'une matrice vide
    array.append([])

for i in range(40): 
    if i == 30: # case allez en prison
        array[i] = 10*[0]+[1]+29*[0]
    else:
        premier_rang = (i+2)%40
        rang_sup = 11-(40-premier_rang) # rang de l'élément en case 1 si premier rang >=30 
        for j in range(rang_sup):
            array[i].append(probas_2_de[11-(rang_sup-j)])
            if j == 10:
                array[i].insert(0,probas_2_de[0])
        
        if rang_sup<=0:
            for k in range(premier_rang):
                array[i].append(0)
            for proba in probas_2_de:
                array[i].append(proba)
        else:
            for k in range(premier_rang-rang_sup):
                array[i].append(0)
            for l in range(11-rang_sup):
                array[i].append(probas_2_de[l])
        for m in range(40-len(array[i])):
            array[i].append(0)
        
        for coord_chance in [8-1,23-1,37-1]: # probabilité si on peut allez vers une case carte chance, la liste correspond aux coordonnées des cases chances sur le plateau
            if array[i][coord_chance] > 0:
                p = array[i][coord_chance] 
                for coord_deplacement in carte_chance_possibilite:
                    array[i][coord_deplacement] += (1/16)*p
                array[i][coord_chance-3] += (1/16)*p # reculer de 3 cases
                array[i][coord_chance] = p*(9/16) # car 7 possibilités de déplacements (+7/16 p) pour maintenir une proba de 1 sur la row

        for coord_communaute in [3-1,18-1,34-1]: # probabilité si on peut allez vers une case carte communauté, la liste correspond aux coordonnées des cases communautés sur le plateau
            if array[i][coord_communaute] > 0:
                p = array[i][coord_communaute]
                for coord_deplacement in carte_communaute_possibilite:
                    array[i][coord_deplacement] += (1/16)*p
                array[i][coord_communaute] = p*(13/16) # car 3 possibilités de déplacements (+3/16 p) pour maintenir une proba de 1 sur la row

A = np.array(array)

# Random Walk on Markov Chain
'''
n = 10
start_state = 0
curr_state = start_state
print(state[curr_state+1][0], "--->", end=" ")

while n-1:
    curr_state = np.random.choice(range(40), p=A[curr_state])
    print(state[curr_state+1][0], "--->", end=" ")
    n-=1
print("stop")'''

# Methode de Monte Carlo pour déterminer une distribution stationnaire

steps = 10**6
start_state = 0
curr_state = start_state
pi = np.array(40*[0])
pi[start_state] = 1

i = 0
while i<steps:
    curr_state = np.random.choice(range(40), p=A[curr_state])
    pi[curr_state]+=1
    i +=1

matrix = list(pi/steps) # distribution stationnaire


# Création d'un classement 

for i in range(len(matrix)):
    state[i+1].append(matrix[i])

classement_cases = sorted(state.values(), key=lambda x:x[1], reverse=True)

print("\n == Classement == ",end="\n\n")

for i in range(40):
    print(i+1, end=".  ")
    print(classement_cases[i][0], end="  ")
    print(classement_cases[i][1],end="\n")

