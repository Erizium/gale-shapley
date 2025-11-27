import random

class Etudiant:
    """
    Représente un étudiant
    """
    def __init__(self, id_etudiant, nom=""):
        self.id = id_etudiant
        self.nom = f"Etu_{id_etudiant}"
        self.liste_voeux = [] # liste des préférences des étudiants
        self.etablissement_affecte = None # stocker l'affectation finale

    def __repr__(self):
        return f"{self.nom}"
        
class Etablissement:
    """
    Représente un établissement avec capacité d'accueil
    """
    def __init__(self, id_etab, capacite=1, nom=""):
        self.id = id_etab
        self.nom = f"Univ_{id_etab}"
        self.capacite = capacite
        self.liste_voeux = [] # liste des étudiants préférés ordonnés
        self.etudiants_affectes = [] # liste des étudiants actuellement acceptés

    def est_plein(self):
        """Retourne Vrai si l'établissement a atteint sa capacité maximale."""
        return len(self.etudiants_affectes) >= self.capacite

    def pire_etudiant_actuel(self):
        """
        Retourne l'étudiant le moins bien classé parmi ceux actuellement affectés
        Ici, on utilisera l'index dans la liste de voeux pour comparer
        """
        if not self.etudiants_affectes:
            return None
        
        # on cherche celui qui a l'index le plus grand dans la liste de voeux (donc le moins aimé)
        pire = max(self.etudiants_affectes, key=lambda e: self.liste_voeux.index(e))
        return pire

    def __repr__(self):
        return f"{self.nom}(capacité:{self.capacite})"

def generer_donnees(nb_etudiants, nb_etablissements, capacites, mode='aleatoire', correlation_strength=0.0):
    """
    Génère les objets Etudiants et Etablissements avec leurs préférences.
    """
    
    # on instancie les étudiants et les établissements
    etudiants = [Etudiant(i) for i in range(nb_etudiants)]
    etablissements = []
    
    for j in range(nb_etablissements):
        cap = capacites if isinstance(capacites, int) else capacites[j]
        etablissements.append(Etablissement(j, capacite=cap))

    # on génère les preferences en fonction du mode
    if mode == 'aleatoire':
        _generer_preferences_uniformes(etudiants, etablissements)
    elif mode == 'correlee':
        _generer_preferences_correlees(etudiants, etablissements, correlation_strength)
    else:
        raise ValueError("Mode inconnu. Choisir 'aleatoire' ou 'correlee' !!")

    return etudiants, etablissements

def _generer_preferences_uniformes(etudiants, etablissements):
    """
    Génération aléatoire uniforme : chaque permutation a la même proba
    """
    # pour chaque étudiant, on mélange la liste des établissements
    for etu in etudiants:
        voeux = list(etablissements)
        random.shuffle(voeux)
        etu.liste_voeux = voeux

    # pour chaque établissement, on mélange la liste des étudiants
    for etab in etablissements:
        voeux = list(etudiants)
        random.shuffle(voeux)
        etab.liste_voeux = voeux

def _generer_preferences_correlees(etudiants, etablissements, strength):
    """
    Génération corrélée (cf rapport pour plus de détails)
    strength : 0 -> bruit total (aléatoire), 1 -> bruit nul (tout le monde a le même classement)
    """
    # on attribue un 'score de qualité' intrinsèque à chaque entité (0 à 1)
    # plus le score est haut, plus l'entité est désirable
    scores_etudiants = {e.id: random.random() for e in etudiants}
    scores_etablissements = {s.id: random.random() for s in etablissements}

    # fct utilitaire pour trier avec bruit
    def get_noisy_score(base_score, noise_factor):
        # le bruit réduit l'impact du score de base
        # noise_factor grand (strength petit) => classement chaotique
        bruit = random.gauss(0, 1) * (1 - strength) 
        return base_score * strength + bruit

    # prefs des étudiants (classent les établissements par score décroissant + bruit)
    for etu in etudiants:
        # on calcule un score perçu pour chaque établissement
        etab_scores = []
        for etab in etablissements:
            perceived_value = get_noisy_score(scores_etablissements[etab.id], strength)
            etab_scores.append((etab, perceived_value))
        
        # Tri décroissant selon la valeur perçue
        etab_scores.sort(key=lambda x: x[1], reverse=True)
        etu.liste_voeux = [x[0] for x in etab_scores]

    # prefs des établissements (classent les étudiants par score décroissant + bruit)
    for etab in etablissements:
        etu_scores = []
        for etu in etudiants:
            perceived_value = get_noisy_score(scores_etudiants[etu.id], strength)
            etu_scores.append((etu, perceived_value))
        
        etu_scores.sort(key=lambda x: x[1], reverse=True)
        etab.liste_voeux = [x[0] for x in etu_scores]

# test rapide 
if __name__ == "__main__":
    print("--- Test de génération ---")
    nb_etudiants = 10
    nb_etablissements = 10
    capacite = 1
    
    E, S = generer_donnees(nb_etudiants, nb_etablissements, capacite, mode='aleatoire')

    print("---------------------------------------------------")
    print("--------------GENERATION UNIFORME------------------")
    print("---------------------------------------------------")
    
    print("--------------ETUDIANTS------------------")
    print(f"Génération uniforme: Etudiant 0 préfère {[e.id for e in E[0].liste_voeux]}")
    print(f"Génération uniforme: Etudiant 1 préfère {[e.id for e in E[1].liste_voeux]}")
    print(f"Génération uniforme: Etudiant 2 préfère {[e.id for e in E[2].liste_voeux]}")

    print("--------------ETABLISSEMENTS------------------")
    print(f"Génération uniforme: Etablissement 0 préfère {[e.id for e in S[0].liste_voeux]}")
    print(f"Génération uniforme: Etablissement 1 préfère {[e.id for e in S[1].liste_voeux]}")
    print(f"Génération uniforme: Etablissement 2 préfère {[e.id for e in S[2].liste_voeux]}")

    print("---------------------------------------------------")
    print("--------------GENERATION CORRELÉE------------------")
    print("---------------------------------------------------")

    print("--------------ETUDIANTS------------------")
    E, S = generer_donnees(nb_etudiants, nb_etablissements, capacite, mode='correlee', correlation_strength=0.9)
    print(f"Génération corrélée (forte): Etudiant 0 préfère {[e.id for e in E[0].liste_voeux]}")
    print(f"Génération corrélée (forte): Etudiant 1 préfère {[e.id for e in E[1].liste_voeux]}")
    print(f"Génération corrélée (forte): Etudiant 2 préfère {[e.id for e in E[2].liste_voeux]}")

    print("--------------ETABLISSEMENTS------------------")
    print(f"Génération corrélée (forte): Etablissement 0 préfère {[e.id for e in S[0].liste_voeux]}")
    print(f"Génération corrélée (forte): Etablissement 1 préfère {[e.id for e in S[1].liste_voeux]}")
    print(f"Génération corrélée (forte): Etablissement 2 préfère {[e.id for e in S[2].liste_voeux]}")