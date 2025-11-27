import generation_preferences
import gale_shapley
import metriques
import plots
import random

def executer_test(nom_test, nb_etudiants, nb_etablissements, capacites, mode_gen='aleatoire', correlation_strength=0.9):
    print(f"\n--- Lancement du {nom_test} ---")
    print(f"Config: {nb_etudiants} étudiants, {nb_etablissements} facs, Capacité {capacites}, Mode {mode_gen}")

    # 1. Génération
    etudiants, etablissements = generation_preferences.generer_donnees(
        nb_etudiants, nb_etablissements, capacites, mode=mode_gen, correlation_strength=correlation_strength
    )
    
    # 2. Algo 1 : etudiant proposant (GS-Etu)
    print("-> Exécution Gale-Shapley (Etudiant Proposant)...")
    gale_shapley.mariage_stable_etudiant_proposant(etudiants, etablissements)
    
    # check stabilité
    instabilites = metriques.compter_paires_instables(etudiants, etablissements)
    if instabilites > 0:
        print(f"ALERTE: {instabilites} paires instables trouvées !")
    
    stats_etu_prop = metriques.calculer_satisfaction_etudiants(etudiants)
    #stats_etu_prop_etab = metriques.calculer_satisfaction_etablissements(etablissements)

    print(f"   Rang moyen étudiants: {stats_etu_prop['rang_moyen']:.2f}")
    print(f"   Nombre d'étudiants non affectés: {stats_etu_prop['nb_non_affectes']}")
    print(f"   Distribution des rangs: {stats_etu_prop['distribution_rangs']}")
    print(f"Insitabilités: {instabilites}")
    
    # 3. Algo 2 : Université Proposant (GS-Univ)
    print("-> Exécution Gale-Shapley (Univ Proposant)...")


    gale_shapley.mariage_stable_universite_proposant(etudiants, etablissements)


    instabilites = metriques.compter_paires_instables(etudiants, etablissements)
    stats_univ_prop = metriques.calculer_satisfaction_etudiants(etudiants)
    
    print(f"   Rang moyen établissements: {stats_univ_prop['rang_moyen']:.2f}")
    # print(f"   Distribution des rangs: {stats_univ_prop['distribution_rangs']}")
    
    print(f"Insitabilités: {instabilites}")

    # 4. Plots
    # on affiche l'histogramme pour ce cas précis
    plots.afficher_comparaison_rangs(
        stats_etu_prop['distribution_rangs'], 
        stats_univ_prop['distribution_rangs'],
        nom_test
    )
    
    return (nom_test, stats_etu_prop['rang_moyen'], stats_univ_prop['rang_moyen'])

if __name__ == "__main__":
    resultats_globaux = []


    # Pour une question de lisibilité on va simuler avec des petites populations 
    
    # --- CAS 1 : N étudiants, N universités, Capacité 1 ---
    N = 30
    res1 = executer_test("CAS 1 - Bijection Parfaite (N=30, M=30, Cap=1)", nb_etudiants=N, nb_etablissements=N, capacites=1)
    resultats_globaux.append(res1)
    
    # --- CAS 2 : N étudiants, M universités, Capacité 1 ---
    N = 30
    M = 10
    res2 = executer_test("CAS 2 - Tension (N=30, M=10, Cap=1)", nb_etudiants=N, nb_etablissements=M, capacites=1)
    resultats_globaux.append(res2)


    # On va simuler deux cas : etablissements selectifs et etablissements non selectifs
    # --- CAS 3 : N étudiants, M universités, Capacité Mi ---
    N = 30
    M = 10
    # etablissements selectifs
    caps = [random.randint(1, 2) for _ in range(M)] 
    res3 = executer_test("CAS 3 - Etablissements Selectifs (N=30, M=10, Cap=Mi)", nb_etudiants=N, nb_etablissements=M, capacites=caps)
    resultats_globaux.append(res3)

    # etablissements non selectifs
    caps = [random.randint(3, 4) for _ in range(M)] 
    res4 = executer_test("CAS 4_bis- Etablissements Non Selectifs (N=30, M=10, Cap=Mi [3,4])", nb_etudiants=N, nb_etablissements=M, capacites=caps)
    resultats_globaux.append(res4)

    
    
    # --- CAS 5 : Préférences Corrélées ---

    # COMPETITION FORTE
    # Ici encore on va simuler le cas où:
    # Beaucoup d'étudiants veulent les mêmes établissements et les etablissements les mêmes étudiants comme Parcoursup
    N=30
    M=10
    corr = 0.9
    res4 = executer_test("CAS Compétition Forte (N=30,M=10,Cap=1)", nb_etudiants=N, nb_etablissements=M, capacites=1, mode_gen='correlee', correlation_strength=corr)
    resultats_globaux.append(res4)


    plots.afficher_comparaison_rang_moyen(resultats_globaux)