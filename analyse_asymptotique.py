import generation_preferences
import gale_shapley
import metriques
import matplotlib.pyplot as plt
import math
from matplotlib.patches import Patch
from matplotlib.lines import Line2D



# GENERATION PIRE ET MEILLEUR CAS

def generer_meilleur_cas(N):
    """
    Génère etudiants et etablissements avec un alignement parfait complexité en O(N)
    cf chaque étudiant i veut l'école i, et l'école i veut l'étudiant i
    Du coup tout le monde est accepté du premier coup
    """
    etudiants = [generation_preferences.Etudiant(i) for i in range(N)]
    etablissements = [generation_preferences.Etablissement(j, capacite=1) for j in range(N)]
    
    for i in range(N):
        # l'étudiant i met l'école i en premier
        # (pas d'importance pour le reste de la lste)
        autres_ecoles = [etablissements[j] for j in range(N) if j != i]
        etudiants[i].liste_voeux = [etablissements[i]] + autres_ecoles
        
        # l'établissement i met l'étudiant i en premier
        autres_etudiants = [etudiants[j] for j in range(N) if j != i]
        etablissements[i].liste_voeux = [etudiants[i]] + autres_etudiants
        
    return etudiants, etablissements

def generer_pire_cas(N):
    """
    On génère une instance O(N^2)
    Idée : forte congestion & préférences inversées
    - tous les étudiants ont la MÊME liste : [0, 1, 2, ..., N]
    - toutes les écoles ont la liste INVERSE : [N, N-1, ..., 0]
    
    Si on déourle : 
    Tout le monde postule à l'établissement 0. Donc l'établissement 0 rejette N-1 élèves
    Ces N-1 vont postulent 1, qui rejette N-2 personnes, etc.
    Cf: somme arithmétique : N + (N-1) + ... + 1 = N(N+1)/2 = O(N^2).
    """
    etudiants = [generation_preferences.Etudiant(i) for i in range(N)]
    etablissements = [generation_preferences.Etablissement(j, capacite=1) for j in range(N)]
    
    # etudiants : CONFLIT MAX (tout le monde veut les mêmes écoles dans le même ordre)
    liste_ecoles_conflit = [etablissements[j] for j in range(N)]
    for etu in etudiants:
        etu.liste_voeux = list(liste_ecoles_conflit)
        
    # etablissement : PREF INVERSES par rapport aux préférences des étudiants
    # Ils préfèrent tous les étudiants qui postuleront en dernier
    liste_etudiants_inverse = [etudiants[i] for i in range(N-1, -1, -1)]
    for etab in etablissements:
        etab.liste_voeux = list(liste_etudiants_inverse)
        
    return etudiants, etablissements


# ANALYSE ET PLOT

def analyse_complete_complexite():
    """
    Exécute les 3 scénarios et affiche les courbes comparatives
    """
    # on va choisir des N assez grands pour capturer la divergence
    nb_max_iter = 450
    pas = 30
    tailles_N = [i for i in range(10, nb_max_iter, pas)] 
    
    res_meilleur = []
    res_moyen = []
    res_pire = []
    
    print("\n--- Lancement de l'Analyse Asymptotique (Nombre d'itérations) ---")
    
    for N in tailles_N:
        #MEILLEUR CAS
        E, S = generer_meilleur_cas(N)
        iter_best = gale_shapley.mariage_stable_etudiant_proposant(E, S)
        res_meilleur.append(iter_best)
        
        #CAS MOYEN (on va faire une moyenne sur 10 itérations pour lisser)
        somme = 0
        nb_essais = 10
        for _ in range(nb_essais):
            E, S = generation_preferences.generer_donnees(N, N, 1, mode='aleatoire')
            somme += gale_shapley.mariage_stable_etudiant_proposant(E, S)
        res_moyen.append(somme / nb_essais)
        
        #Pire Cas
        E, S = generer_pire_cas(N)
        iter_worst = gale_shapley.mariage_stable_etudiant_proposant(E, S)
        res_pire.append(iter_worst)
        
        print(f" Nb itérations pour N={N} étudiants: Meilleur={iter_best} | Moyen={res_moyen[-1]:.1f} | Pire={iter_worst}")


    # PLOTS DES COMPLEXITES

    plt.figure(figsize=(12, 8))
    
    #  courbes experimentales
    plt.plot(tailles_N, res_pire, 's-', color='#e74c3c', label='Pire Cas (Expérimental)', linewidth=2)
    plt.plot(tailles_N, res_moyen, 'o-', color='#3498db', label='Cas Moyen (Expérimental)', linewidth=2)
    plt.plot(tailles_N, res_meilleur, '^-', color='#2ecc71', label='Meilleur Cas (Expérimental)', linewidth=2)
    
    # coubres théoriques en pointillés
    
    # théorie N^2/2 (somme arithmétique observée dans le pire cas)
    y_n2 = [(n*n)/2 for n in tailles_N]
    plt.plot(tailles_N, y_n2, '--', color='maroon', alpha=0.6, label=r'Théorie $O(N^2/2)$')
    
    # théorie N log N 
    # on ajoute un coefficient k ajusté sur le dernier point pour superposer les échelles
    if tailles_N[-1] > 0:
        val_ref = tailles_N[-1] * math.log(tailles_N[-1])
        k = res_moyen[-1] / val_ref
        y_nlogn = [k * n * math.log(n) for n in tailles_N]
        plt.plot(tailles_N, y_nlogn, '--', color='navy', alpha=0.6, label=r'Théorie $O(N \ln N)$')
    
    # théorie N (Meilleur cas)
    y_n = [n for n in tailles_N]
    plt.plot(tailles_N, y_n, '--', color='darkgreen', alpha=0.6, label=r'Théorie $O(N)$')

    plt.xlabel(f'Nombre d\'étudiants')
    plt.ylabel('Nombre d\'itérations')
    plt.title('Analyse de la Complexité Temporelle de Gale-Shapley')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.savefig('analyse_complexite.png')
    plt.show()


def analyse_ratio_tension():
    """
    Analyse fine de l'impact du ratio N/M sur la satisfaction
    Focus sur la zone de transition autour de 1
    """
    M = 50 # on prend un M raisonnable pour avoir de la granularité
    
    # on teste des ratios de 0.5 (sous-tension) à 2.5 (sur-tension)
    # EX: 0.5 -> 25 étudiants pour 50 places
    # EX: 2.0 -> 100 étudiants pour 50 places
    ratios = [x / 10.0 for x in range(5, 30, 2)] # [0.5, 0.7, ..., 2.9]
    
    rangs_moyens = []
    pourcentage_satisfaction = [] # Nouvelle métrique intéressante !
    
    print("\n--- Analyse du Ratio N/M (Tension) ---")
    
    for r in ratios:
        N = int(M * r)
        E, S = generation_preferences.generer_donnees(N, M, 1, mode='aleatoire')
        gale_shapley.mariage_stable_etudiant_proposant(E, S)
        
        stats = metriques.calculer_satisfaction_etudiants(E)
        rangs_moyens.append(stats['rang_moyen'])
        
        # calcule le nombre d'étudiants qui ont eu leur 1er vœu
        nb_v1 = stats['distribution_rangs'].get(1, 0)
        # nb total d'étudiants affectés
        nb_affectes = len(E) - stats['nb_non_affectes']
        # % de satisfaction (ceux qui ont eu leur 1er vœu)
        pourcentage = (nb_v1 / nb_affectes * 100) if nb_affectes > 0 else 0.0
        pourcentage_satisfaction.append(pourcentage)
        
        print(f"Ratio={r:.1f} (N={N}/M={M}): Rang Moyen={stats['rang_moyen']:.2f} | % 1er vœu={pourcentage:.1f}% ({nb_v1}/{nb_affectes})")

    # Plot avec double axe Y : Rang moyen et % de satisfaction
    _, ax1 = plt.subplots(figsize=(12, 7))
    
    # Premier axe Y : Rang moyen
    color1 = 'purple'
    ax1.set_xlabel('Ratio Tension (Nb Etudiants / Nb Places)', fontsize=12)
    ax1.set_ylabel('Rang Moyen (plus bas = mieux)', color=color1, fontsize=12)
    line1 = ax1.plot(ratios, rangs_moyens, 'o-', color=color1, linewidth=2, markersize=8, label='Rang Moyen')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)
    
    # Deuxième axe Y : % de satisfaction (1er vœu)
    ax2 = ax1.twinx()
    color2 = 'teal'
    ax2.set_ylabel('% Étudiants ayant obtenu leur 1er vœu', color=color2, fontsize=12)
    line2 = ax2.plot(ratios, pourcentage_satisfaction, 's-', color=color2, linewidth=2, markersize=8, label='% 1er vœu')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim([0, 100])  # Pourcentage de 0 à 100%
    
    # Zone de confort (N < M) vs Zone de tension (N > M)
    ax1.axvline(x=1.0, color='red', linestyle='--', linewidth=2, alpha=0.7, zorder=0)
    ax1.axvspan(0.5, 1.0, alpha=0.1, color='green', zorder=0)
    ax1.axvspan(1.0, max(ratios), alpha=0.1, color='orange', zorder=0)

    # Annotation pour le point de bascule
    ax1.text(1.0, ax1.get_ylim()[1] * 0.95, 'N=M', rotation=90, 
             verticalalignment='top', horizontalalignment='right', 
             color='red', fontweight='bold', fontsize=10)
    
    ax1.set_title('Transition de phase : Impact de la tension sur la satisfaction', fontsize=14, fontweight='bold')
    
    # Légende combinée pour les deux axes + zones

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    # Ajouter les zones et la ligne de bascule à la légende
    legend_elements = [
        Patch(facecolor='green', alpha=0.3, label='Sous-tension (Places libres)'),
        Patch(facecolor='orange', alpha=0.3, label='Sur-tension (Compétition)'),
        Line2D([0], [0], color='red', linestyle='--', linewidth=2, label='Point de Bascule (N=M)'),
    ]
    ax1.legend(lines + legend_elements, labels + [le.get_label() for le in legend_elements], 
               loc='upper left', fontsize=10, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig('analyse_ratio_tension.png')
    plt.show()
    
def analyse_impact_structurel():
    """
    Analyse "Iso-Offre" : On garde le nombre TOTAL de places constant et égal au nombre d'étudiants.
    On fait varier la structure du marché : de "Atomisé" (plein de petites facs) à "Centralisé" (peu de grosses facs).
    
    Hypothèse : Les gros établissements agissent comme des "tampons" qui absorbent mieux les vœux
    et stabilisent le marché plus vite, améliorant le rang moyen.
    """
    N = 500
    places_totales = 500  # On est à l'équilibre parfait
    
    # On teste différentes configurations (M * q = 500)
    # (Nb Etablissements, Capacité par établissement)
    configs = [
        (500, 1),   # Marché très fragmenté (style lycées...)
        (250, 2),
        (100, 5),
        (50, 10),
        (25, 20),
        (10, 50),
        (5, 100),
        (2, 250),
        (1, 500)    # Marché monolithique (style facs)
    ]
    
    capacites_x = []
    rangs_moyens_y = []
    
    print("\n--- Analyse Structurelle (Iso-Offre) ---")
    print(f"Population : {N} étudiants pour {places_totales} places au total.")
    
    for M, q in configs:
        # On lisse sur plusieurs essais car l'aléatoire joue beaucoup quand M est petit
        somme_rangs = 0
        nb_essais = 10
        
        for _ in range(nb_essais):
            E, S = generation_preferences.generer_donnees(N, M, q, mode='aleatoire')
            gale_shapley.mariage_stable_etudiant_proposant(E, S)
            stats = metriques.calculer_satisfaction_etudiants(E)
            somme_rangs += stats['rang_moyen']
            
        moyenne = somme_rangs / nb_essais
        
        capacites_x.append(q)
        rangs_moyens_y.append(moyenne)
        
        print(f"Config {M} écoles de {q} places : Rang Moyen = {moyenne:.2f}")

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # On utilise une échelle log pour l'axe X car la capacité varie de 1 à 500
    ax.plot(capacites_x, rangs_moyens_y, 'o-', color='teal', linewidth=2, markersize=8)
    ax.set_xscale('log') 
    
    ax.set_xlabel('Capacité par établissement (échelle log)')
    ax.set_ylabel('Rang Moyen (Satisfaction)')
    ax.set_title(f'Impact de la granularité de l\'offre (N={N}, Places={places_totales})')
    
    # annotations pour comprendre le graph
    ax.text(capacites_x[0], rangs_moyens_y[0]+0.5, "Marché Fragmenté\n(Bcp de petites écoles)", ha='left')
    ax.text(capacites_x[-1], rangs_moyens_y[-1]+0.5, "Marché Centralisé\n(Peu de grosses écoles)", ha='right')
    
    ax.grid(True, which="both", ls="-", alpha=0.5)
    plt.savefig('analyse_impact_structurel.png')
    plt.show()

if __name__ == "__main__":
    # lancer les analyses
    analyse_complete_complexite()
    analyse_ratio_tension()
    analyse_impact_structurel()