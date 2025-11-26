import matplotlib.pyplot as plt

def afficher_comparaison_rangs(distrib_etu_prop, distrib_univ_prop, titre):
    """
    Affiche un histogramme comparant les rangs obtenus par les étudiants
    selon qui propose (Etudiant ou Université).
    """
    # on récupère tous les rangs possibles (les clés des dictionnaires)
    rangs = sorted(list(set(distrib_etu_prop.keys()) | set(distrib_univ_prop.keys())))
    
    # on prépare les listes pour le plot
    valeurs_etu = [distrib_etu_prop.get(r, 0) for r in rangs]
    valeurs_univ = [distrib_univ_prop.get(r, 0) for r in rangs]
    
    x = range(len(rangs))
    width = 0.35  # largeur des barres

    _, ax = plt.subplots(figsize=(10, 6))
    
    # on dessine les barres
    ax.bar([i - width/2 for i in x], valeurs_etu, width, label='Etudiant Proposant', color='skyblue')
    ax.bar([i + width/2 for i in x], valeurs_univ, width, label='Univ Proposant', color='salmon')

    # labels et titres
    ax.set_xlabel('Rang du vœu obtenu')
    ax.set_ylabel('Nombre d\'étudiants')
    ax.set_title(f'Comparaison des satisfactions - {titre}')
    ax.set_xticks(x)
    ax.set_xticklabels(rangs)
    ax.legend()

    # petit ajout pour afficher le nombre au dessus des barres
    # ne pas afficher le nombre pour les barres qui sont à 0
    for i, v in enumerate(valeurs_etu):
        if v > 0:
            ax.text(i, v, v, ha='center', va='bottom')
    for i, v in enumerate(valeurs_univ):
        if v > 0:
            ax.text(i, v, v, ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(f'{titre}.png')
    plt.show()


import matplotlib.pyplot as plt
import numpy as np # Utile pour gérer les positions des barres proprement

def afficher_comparaison_rangs(distrib_etu_prop, distrib_univ_prop, titre):
    """
    Affiche un histogramme comparant les rangs obtenus par les étudiants
    selon qui propose (Etudiant ou Université).
    """
    rangs = sorted(list(set(distrib_etu_prop.keys()) | set(distrib_univ_prop.keys())))
    
    valeurs_etu = [distrib_etu_prop.get(r, 0) for r in rangs]
    valeurs_univ = [distrib_univ_prop.get(r, 0) for r in rangs]
    
    x = range(len(rangs))
    width = 0.35 

    fig, ax = plt.subplots(figsize=(10, 6))
    
    rects1 = ax.bar([i - width/2 for i in x], valeurs_etu, width, label='Etudiant Proposant', color='skyblue')
    rects2 = ax.bar([i + width/2 for i in x], valeurs_univ, width, label='Univ Proposant', color='salmon')

    ax.set_xlabel('Rang du vœu obtenu')
    ax.set_ylabel('Nombre d\'étudiants')
    ax.set_title(f'Distribution des rangs Étudiants - {titre}')
    ax.set_xticks(x)
    ax.set_xticklabels(rangs)
    ax.legend()

    # on ajoute les labels
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    plt.tight_layout()
    plt.savefig(f'{titre}.png')
    plt.show()

def afficher_analyse_croisee(resultats_complets):
    """
    Affiche un graphique groupé pour vérifier la théorie :
    L'optimalité pour l'un est le pire cas pour l'autre.
    
    resultats_complets est une liste de dict contenant les rangs moyens pour chaque config.
    """
    noms_tests = [r['nom'] for r in resultats_complets]
    
    # On récupère les 4 métriques clés
    etu_gs_etu = [r['etu_dans_gs_etu'] for r in resultats_complets] # Optimal Etu
    etu_gs_univ = [r['etu_dans_gs_univ'] for r in resultats_complets] # Pessimal Etu
    
    univ_gs_etu = [r['univ_dans_gs_etu'] for r in resultats_complets] # Pessimal Univ
    univ_gs_univ = [r['univ_dans_gs_univ'] for r in resultats_complets] # Optimal Univ
    
    x = np.arange(len(noms_tests))
    width = 0.2  # on a 4 barres, donc il faut qu'elles soient fines

    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Barres pour les étudiants (Teintes de Bleu)
    rects1 = ax.bar(x - 1.5*width, etu_gs_etu, width, label='Satisfaction Etu (si Etu Propose)', color='#3498db')
    rects2 = ax.bar(x - 0.5*width, etu_gs_univ, width, label='Satisfaction Etu (si Univ Propose)', color='#aed6f1')
    
    # Barres pour les universités (Teintes de Rouge)
    rects3 = ax.bar(x + 0.5*width, univ_gs_etu, width, label='Satisfaction Univ (si Etu Propose)', color='#f5b7b1')
    rects4 = ax.bar(x + 1.5*width, univ_gs_univ, width, label='Satisfaction Univ (si Univ Propose)', color='#e74c3c')

    ax.set_ylabel('Rang Moyen (plus bas = meilleur)')
    ax.set_title('Validation Théorique : Comparaison Croisée des Satisfactions')
    ax.set_xticks(x)
    ax.set_xticklabels(noms_tests, rotation=15, ha="right")
    ax.legend()
    
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig('comparaison_croisee.png')
    plt.show()