import generation_preferences
import gale_shapley
import metriques
import plots
import random

def executer_test(nom_test, nb_etudiants, nb_etablissements, capacites, mode_gen='aleatoire', correlation_strength=0.9):
    print(f"\n==================================================")
    print(f"--- Lancement du {nom_test} ---")
    print(f"Config: {nb_etudiants} étudiants, {nb_etablissements} facs, Capacité {capacites}, Mode {mode_gen}")

    # 1. Génération
    etudiants, etablissements = generation_preferences.generer_donnees(
        nb_etudiants, nb_etablissements, capacites, mode=mode_gen, correlation_strength=correlation_strength
    )
    
    # =========================================================
    # 2. Algo 1 : Etudiant Proposant (GS-Student)
    # =========================================================
    print("\n-> Exécution Gale-Shapley (Etudiant Proposant)...")
    gale_shapley.mariage_stable_etudiant_proposant(etudiants, etablissements)
    
    # On calcule les stats pour TOUT LE MONDE dans ce scénario
    stats_etu_dans_gs_etu = metriques.calculer_satisfaction_etudiants(etudiants)
    stats_univ_dans_gs_etu = metriques.calculer_satisfaction_etablissements(etablissements) 
    
    instabilites = metriques.compter_paires_instables(etudiants, etablissements)

    print(f"Insitabilités: {instabilites}")
    print(f"Rang moyen étudiants: {stats_etu_dans_gs_etu['rang_moyen']:.2f}")
    print(f"Regret max étudiants: {stats_etu_dans_gs_etu['regret_max']}")
    print(f"Ecart-type étudiants: {stats_etu_dans_gs_etu['ecart_type']:.2f}")
    print(f"Nombre d'étudiants non affectés: {stats_etu_dans_gs_etu['nb_non_affectes']}")


    print(f"Rang moyen établissements: {stats_univ_dans_gs_etu['rang_moyen']:.2f}")
    print(f"Regret max établissements: {stats_univ_dans_gs_etu['regret_max']}")
    print(f"Ecart-type établissements: {stats_univ_dans_gs_etu['ecart_type']:.2f}")

    # =========================================================
    # 3. Algo 2 : Université Proposant (GS-Univ)
    # =========================================================
    print("\n-> Exécution Gale-Shapley (Univ Proposant)...")
    # L'algo doit reset l'état interne, on suppose que ta fonction le fait (reset_etat)
    gale_shapley.mariage_stable_universite_proposant(etudiants, etablissements)

    # On calcule les stats pour TOUT LE MONDE dans ce scénario
    # ATTENTION : On utilise des NOUVELLES variables
    stats_etu_dans_gs_univ = metriques.calculer_satisfaction_etudiants(etudiants)
    stats_univ_dans_gs_univ = metriques.calculer_satisfaction_etablissements(etablissements)

    instabilites = metriques.compter_paires_instables(etudiants, etablissements)

    print(f"Insitabilités: {instabilites}")
    print(f"Rang moyen étudiants: {stats_etu_dans_gs_univ['rang_moyen']:.2f}")
    print(f"Regret max étudiants: {stats_etu_dans_gs_univ['regret_max']}")
    print(f"Ecart-type étudiants: {stats_etu_dans_gs_univ['ecart_type']:.2f}")
    print(f"Nombre d'étudiants non affectés: {stats_etu_dans_gs_univ['nb_non_affectes']}")

    print(f"Rang moyen établissements: {stats_univ_dans_gs_univ['rang_moyen']:.2f}")
    print(f"Regret max établissements: {stats_univ_dans_gs_univ['regret_max']}")
    print(f"Ecart-type établissements: {stats_univ_dans_gs_univ['ecart_type']:.2f}")

    # 4. Plots spécifique à ce cas (Distribution des rangs étudiants uniquement)
    plots.afficher_comparaison_rangs(
        stats_etu_dans_gs_etu['distribution_rangs'], 
        stats_etu_dans_gs_univ['distribution_rangs'],
        nom_test
    )
    
    # On retourne un dictionnaire complet avec les 4 métriques croisées
    return {
        "nom": nom_test,
        "etu_dans_gs_etu": stats_etu_dans_gs_etu['rang_moyen'],       # Théoriquement le MEILLEUR score (bas)
        "univ_dans_gs_etu": stats_univ_dans_gs_etu['rang_moyen'],     # Théoriquement le PIRE score (haut)
        "etu_dans_gs_univ": stats_etu_dans_gs_univ['rang_moyen'],     # Théoriquement le PIRE score (haut)
        "univ_dans_gs_univ": stats_univ_dans_gs_univ['rang_moyen']    # Théoriquement le MEILLEUR score (bas)
    }




if __name__ == "__main__":
    resultats_globaux = []
    
    # --- CAS 1 : Bijection (Le cas témoin pour voir l'asymétrie) ---
    N = 50
    res1 = executer_test("CAS 1 - Bijection (N=50)", nb_etudiants=N, nb_etablissements=N, capacites=1)
    resultats_globaux.append(res1)
    
    # --- CAS 2 : Tension (Plus d'étudiants que de places) ---
    N = 50
    M = 20
    res2 = executer_test("CAS 2 - Tension (N=50, M=20)", nb_etudiants=N, nb_etablissements=M, capacites=1)
    resultats_globaux.append(res2)

    # --- CAS 3 : Etablissements Selectifs ---
    N = 50
    M = 10
    caps = [random.randint(2, 3) for _ in range(M)] 
    res3 = executer_test("CAS 3 - Selectifs (N=50, M=10)", nb_etudiants=N, nb_etablissements=M, capacites=caps)
    resultats_globaux.append(res3)

    # --- CAS 4 : Etablissements Non Selectifs ---
    N = 50
    M = 10
    caps = [random.randint(6, 8) for _ in range(M)] 
    res4 = executer_test("CAS 4 - Non Selectifs (N=50, M=10)", nb_etudiants=N, nb_etablissements=M, capacites=caps)
    resultats_globaux.append(res4)
    
    # --- CAS 5 : Compétition Forte ---
    res5 = executer_test("CAS 5 - Correlé (N=50)", nb_etudiants=50, nb_etablissements=20, capacites=1, mode_gen='correlee', correlation_strength=0.9)
    resultats_globaux.append(res5)

    # Affichage de l'analyse croisée finale
    # (Assure-toi que cette fonction est bien dans plots.py)
    plots.afficher_analyse_croisee(resultats_globaux)
