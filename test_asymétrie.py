import generation_preferences
import gale_shapley
import metriques

def test_cas_manuel_asymetrie():
    print("\n==================================================")
    print("--- CAS 6 : Démonstration Manuelle Best/Worst ---")
    
    # Création de 3 étudiants et 3 facs
    E = [generation_preferences.Etudiant(i, nom=f"E{i+1}") for i in range(3)]
    S = [generation_preferences.Etablissement(j, capacite=1, nom=f"Fac{j+1}") for j in range(3)]
    
    # --- PRÉFÉRENCES CONFLICTUELLES (Cycle) ---
    # Les étudiants veulent : 1 > 2 > 3 (décalé)
    # E1 : Fac1 > Fac2 > Fac3
    E[0].liste_voeux = [S[0], S[1], S[2]]
    # E2 : Fac2 > Fac3 > Fac1
    E[1].liste_voeux = [S[1], S[2], S[0]]
    # E3 : Fac3 > Fac1 > Fac2
    E[2].liste_voeux = [S[2], S[0], S[1]]
    
    # Les facs veulent l'inverse :
    # Fac1 : E2 > E3 > E1  (Elle déteste E1 qui l'adore)
    S[0].liste_voeux = [E[1], E[2], E[0]]
    # Fac2 : E3 > E1 > E2
    S[1].liste_voeux = [E[2], E[0], E[1]]
    # Fac3 : E1 > E2 > E3
    S[2].liste_voeux = [E[0], E[1], E[2]]
    
    # 1. Étudiant Proposant
    print("\n[Algo 1] Étudiant Proposant :")
    gale_shapley.mariage_stable_etudiant_proposant(E, S)
    for e in E:
        print(f"  {e.nom} a obtenu {e.etablissement_affecte.nom} (Son vœu n°{e.liste_voeux.index(e.etablissement_affecte)+1})")
    
    stats_e = metriques.calculer_satisfaction_etudiants(E)
    stats_s = metriques.calculer_satisfaction_etablissements(S)
    print(f"  -> Rang Moyen Etudiants: {stats_e['rang_moyen']:.2f} (BEST)")
    print(f"  -> Rang Moyen Facs: {stats_s['rang_moyen']:.2f} (WORST)")

    # 2. Université Proposant
    # Reset manuel nécessaire ici car on réutilise les mêmes objets
    for e in E: e.etablissement_affecte = None
    for s in S: s.etudiants_affectes = []
        
    print("\n[Algo 2] Université Proposant :")
    gale_shapley.mariage_stable_universite_proposant(E, S)
    for s in S:
        # On récupère l'étudiant affecté (capacité 1)
        if s.etudiants_affectes:
            e = s.etudiants_affectes[0]
            print(f"  {s.nom} a obtenu {e.nom} (Son vœu n°{s.liste_voeux.index(e)+1})")
            
    stats_e_2 = metriques.calculer_satisfaction_etudiants(E)
    stats_s_2 = metriques.calculer_satisfaction_etablissements(S)
    print(f"  -> Rang Moyen Etudiants: {stats_e_2['rang_moyen']:.2f} (WORST)")
    print(f"  -> Rang Moyen Facs: {stats_s_2['rang_moyen']:.2f} (BEST)")

if __name__ == "__main__":
    test_cas_manuel_asymetrie()