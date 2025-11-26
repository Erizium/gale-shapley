import generation_preferences

def reset_etat(etudiants, etablissements):
    """
    Fonction pour remettre à zéro les affectations avant de lancer un nouvel algo
    """
    for e in etudiants:
        e.etablissement_affecte = None
    for s in etablissements:
        s.etudiants_affectes = []

def mariage_stable_etudiant_proposant(etudiants, etablissements):
    """
    Implémentation de Gale-Shapley où les étudiants proposent
    """
    reset_etat(etudiants, etablissements)
    
    etudiants_non_affectes = list(etudiants)
    
    # on va mémoriser l'indice du prochain établissement pour lequel l'étudiant va proposer
    # au départ tout les étudiants veulent proposer leur 1er voeu
    index_propositions = {e.id: 0 for e in etudiants}

    # compteur pour la complexité
    nb_propositions = 0 

    while etudiants_non_affectes:
        # on prend le premier étudiant de la liste
        etudiant = etudiants_non_affectes.pop(0)
        
        # on check quelle est le prochain etablissement sur sa liste de voeux
        index_prochaine_proposition = index_propositions[etudiant.id]
        
        # si il a épuisé tous ses voeux il reste evidemment non affecté
        if index_prochaine_proposition >= len(etudiant.liste_voeux):
            continue
            
        etablissement_vise = etudiant.liste_voeux[index_prochaine_proposition]
        
        # on maj l'index de la prochaine proposition (si jamais il est rejeté)
        index_propositions[etudiant.id] += 1
        
        nb_propositions += 1
        
        # CAS 1 : l'etablissement a encore de la place
        if not etablissement_vise.est_plein():
            # on affecte temporairement l'étudiant à l'établissement et on maj l'affectation de l'étudiant
            etablissement_vise.etudiants_affectes.append(etudiant)
            etudiant.etablissement_affecte = etablissement_vise
            
        # CAS 2 : l'établissement est pleine, on compare avec le pire des étudiants affectés actuels
        else:
            pire_admis = etablissement_vise.pire_etudiant_actuel()
            
            # on check la position dans la liste de préférence de l'établissement
            # ie on récupere l'index pour le nouvel et pire étudiant pour comparer
            rang_nouveau = etablissement_vise.liste_voeux.index(etudiant)
            rang_pire = etablissement_vise.liste_voeux.index(pire_admis)
            
            if rang_nouveau < rang_pire:
                
                etablissement_vise.etudiants_affectes.remove(pire_admis)
                pire_admis.etablissement_affecte = None
                
                etablissement_vise.etudiants_affectes.append(etudiant)
                etudiant.etablissement_affecte = etablissement_vise
                
                # le rejeté redevient non affecté
                etudiants_non_affectes.append(pire_admis)
            else:
                # l'étudiant rejeté proposera son prochain voeux (si il lui reste)
                etudiants_non_affectes.append(etudiant)

    return nb_propositions

def mariage_stable_universite_proposant(etudiants, etablissements):
    """
    Implémentation de Gale-Shapley où les établissements proposent
    """

    reset_etat(etudiants, etablissements)

    # liste des établissements qui ont encore des places ET des étudiants à proposer
    etablissements_libres = list(etablissements)
    
    # index pour savoir à quel étudiant l'etablissement doit proposer
    index_propositions = {s.id: 0 for s in etablissements}

    # compteur pour la complexité
    nb_propositions = 0
    
    while etablissements_libres:
        etablissement = etablissements_libres.pop(0)
        
        # si l'etablissement est rempli, il n'a plus besoin de proposer
        if etablissement.est_plein():
            continue
            
        # sinon on regarde le prochain étudiant sur sa liste
        index_prochaine_proposition = index_propositions[etablissement.id]
        
        # si il a fait le tour de tous les étudiants, on arrête pour celui-ci
        if index_prochaine_proposition >= len(etablissement.liste_voeux):
            continue
            
        candidat = etablissement.liste_voeux[index_prochaine_proposition]
        index_propositions[etablissement.id] += 1

        nb_propositions += 1
        
        # on remet l'etablissement dans la file pour qu'il continue de remplir ses places restantes
        etablissements_libres.append(etablissement)
        
        # l'étudiant reçoit la proposition si il n'est pas encore affecté
        if candidat.etablissement_affecte is None:
            # si il est libre il accepte temporairement
            candidat.etablissement_affecte = etablissement
            etablissement.etudiants_affectes.append(candidat)
            
        else:
            # sinon si il est déjà affecté, on compare avec l'établissement actuel
            etablissement_actuel_candidat = candidat.etablissement_affecte
            
            rang_actuel = candidat.liste_voeux.index(etablissement_actuel_candidat)
            rang_nouveau = candidat.liste_voeux.index(etablissement)
            
            if rang_nouveau < rang_actuel:
                # si le candidat préfère le nouvel établissement , on le retire de l'ancien
                etablissement_actuel_candidat.etudiants_affectes.remove(candidat)
                
                # on check si l'acien etablissement était plein (ie pas libre) 
                # alors on le "réactive" psq il vient de perdre un candidat
                if etablissement_actuel_candidat not in etablissements_libres:
                    etablissements_libres.append(etablissement_actuel_candidat)
                
                # le candidat accepte la nouvelle proposition
                candidat.etablissement_affecte = etablissement
                etablissement.etudiants_affectes.append(candidat)
                
            else:
                # Sinon il préfère garder son affectation actuelle, il a rejetté l'offre
                pass

    return nb_propositions