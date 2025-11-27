import statistics

def calculer_satisfaction_etudiants(etudiants):
    """
    Calcule les statistiques de satisfaction pour les étudiants
    """
    nb_etudiants_total = len(etudiants)
    rangs_obtenus = [] 

    for etudiant in etudiants:
        if etudiant.etablissement_affecte is None:
            continue
            
        etablissement_obtenu = etudiant.etablissement_affecte
        # index+1 car le rang commence à 1
        rang = etudiant.liste_voeux.index(etablissement_obtenu) + 1
        rangs_obtenus.append(rang)
            
    if rangs_obtenus:
        rang_moyen = statistics.mean(rangs_obtenus)
        regret_max = max(rangs_obtenus) # Le pire classement obtenu
        # ecart-type (si n > 1 car sinon on a division par 0)
        ecart_type = statistics.stdev(rangs_obtenus) if len(rangs_obtenus) > 1 else 0.0
    else:
        rang_moyen = 0
        regret_max = 0
        ecart_type = 0

    distribution_rangs = {i: 0 for i in range(1, len(etudiants[0].liste_voeux) + 1)}
    for r in rangs_obtenus:
        if r in distribution_rangs:
            distribution_rangs[r] += 1
        else:
            distribution_rangs[r] = 1 

    return {
        "rang_moyen": rang_moyen,
        "regret_max": regret_max,      
        "ecart_type": ecart_type,     
        "distribution_rangs": distribution_rangs,
        "nb_non_affectes": nb_etudiants_total - len(rangs_obtenus)
    }

def calculer_satisfaction_etablissements(etablissements):
    """
    Calcule les statistiques pour les établissements
    """
    rangs_obtenus = []
    
    for etablissement in etablissements:
        for etudiant in etablissement.etudiants_affectes:
            rang = etablissement.liste_voeux.index(etudiant) + 1
            rangs_obtenus.append(rang)
                
    if rangs_obtenus:
        rang_moyen = statistics.mean(rangs_obtenus)
        regret_max = max(rangs_obtenus)
        ecart_type = statistics.stdev(rangs_obtenus) if len(rangs_obtenus) > 1 else 0.0
    else:
        rang_moyen = 0
        regret_max = 0
        ecart_type = 0
    
    # On génère une distribution simplifiée pour les établissements si besoin
    distribution_rangs = {}
    for r in rangs_obtenus:
        distribution_rangs[r] = distribution_rangs.get(r, 0) + 1

    return {
        "rang_moyen": rang_moyen,
        "regret_max": regret_max,
        "ecart_type": ecart_type,
        "distribution_rangs": distribution_rangs
    }

def compter_paires_instables(etudiants, etablissements):
    """
    Vérifie la stabilité
    théoriquement on doit avoir 0 paires instables pour GS
    """
    nb_instabilites = 0
    
    for etudiant in etudiants:
        if etudiant.etablissement_affecte is None:
            continue
            
        etab_actuel = etudiant.etablissement_affecte
        rang_actuel = etudiant.liste_voeux.index(etab_actuel)
        
        # on regarde tous les établissements qu'il préfère à son affectation actuelle
        # ie tous ceux qui sont avant dans sa liste (index < rang_actuel)
        etablissements_preferes = etudiant.liste_voeux[:rang_actuel]
        
        for etab_prefere in etablissements_preferes:
            # Pour qu'il y ait instabilité, il faut que cet etab_prefere préfère aussi cet étudiant
            # à l'un de ceux qu'il a déjà OU qu'il ait de la place libre.
            
            if not etab_prefere.est_plein():
                nb_instabilites += 1
            else:
                pire_admis = etab_prefere.pire_etudiant_actuel()
                # si l'étudiant est mieux classé que le pire des admis de l'école visée
                if etab_prefere.liste_voeux.index(etudiant) < etab_prefere.liste_voeux.index(pire_admis):
                    nb_instabilites += 1

    return nb_instabilites

