# PANAME — Contrat Système

---

## 1. Acteurs

**Humains**
- Admin
- Utilisateurs
- Salons de coiffure

**Systèmes externes**
- Système de génération d'image
- Système de notifications par SMS ou par Email

---

## 2. Promesses (Que promet-on ?)

**Utilisateurs**
- Tester des coiffures virtuellement
- Filtrer les coiffures sur le catalogue
- Prendre un RDV

**Salon**
- Une vitrine numérique à chaque salon de coiffure
- Une notification pour chaque RDV
- Refuser ou accepter un RDV
- Gérer un profil Salon (ajouter des coiffures, voir des commentaires et likes)

**Admin**
- Suspendre un compte
- Voir la liste de tous les comptes
- Lever toutes les sessions et faire une maintenance

---

## 3. Invariants (Que garantit-on — toujours ?)

> Ces règles sont vraies avant, pendant et après chaque opération. Elles ne changent jamais.

- L'authentification est toujours obligatoire pour avoir accès au système
- La sécurité des données est garantie pour tous les acteurs
- Chaque acteur n'a droit qu'à l'interface dont il a l'autorisation
- Un créneau ne peut être réservé que par un seul coiffeur à la fois — même en cas d'accès concurrent
- Une réservation est toujours dans l'un des quatre états valides : En attente · Confirmée · Annulée · Réalisée
- Un avis Utilisateur ne peut exister sans un RDV réalisé avec ce Salon enregistré dans le système
- Une coiffure appartient à exactement un Salon — jamais zéro, jamais deux

---

## 4. Interdictions & Scénarios d'Erreur (Que refuse-t-on strictement ?)

**Accès & Rôles**
- ❌ Un Utilisateur accède à l'interface Salon ou Admin → `403 Interdit`
- ❌ Un Salon accède aux données d'un autre Salon → `403 Interdit`
- ❌ Un Admin modifie directement le catalogue d'un Salon → `403 Interdit`
- ❌ Toute ressource protégée est atteinte sans authentification valide → `401 Non authentifié`

**Comptes**
- ❌ Un Salon suspendu crée de nouvelles entrées dans le catalogue → `403 Compte suspendu`
- ❌ Un Salon suspendu accepte de nouvelles réservations → `403 Compte suspendu`
- ❌ Un Salon suspendu apparaît dans les résultats de recherche → filtré silencieusement

**Catalogue**
- ❌ Une coiffure liée à une réservation active est supprimée → `409 Conflit`
- ❌ Une coiffure désactivée est affichée aux Utilisateurs → filtrée silencieusement
- ❌ Le catalogue contient autre chose que des coiffures africaines → rejeté à la création

**Réservations**
- ❌ Deux réservations sur le même créneau pour le même coiffeur → `409 Créneau non disponible`
- ❌ Une réservation passe directement de En attente à Réalisée → `422 Transition invalide`
- ❌ Toute transition d'état non définie → `422 Transition invalide`

**Données & Vie privée**
- ❌ La photo d'un Utilisateur est conservée au-delà de 24h sans compte actif → supprimée automatiquement
- ❌ La photo d'un Utilisateur est utilisée à d'autres fins que la génération IA sans consentement → bloqué au niveau système
- ❌ Un mot de passe est stocké en clair → rejeté à la persistance
- ❌ Des détails techniques apparaissent dans les messages d'erreur → supprimés avant la réponse

---

## 5. Checklist de Cohérence

**Acteurs & Interactions**
- [x] Tous les acteurs primaires identifiés (Utilisateur, Salon, Admin)
- [x] Tous les systèmes externes identifiés (Génération image, Notifications)
- [x] Rôles définis et séparés

**Actions Autorisées**
- [x] Capacités core listées par acteur
- [x] Éléments hors périmètre v1 identifiés (paiement, app mobile, messagerie)

**Garanties & Invariants**
- [x] Invariants métier listés — chacun vérifiable
- [x] Invariants de sécurité documentés
- [x] Aucune formulation vague

**Interdictions & Exceptions**
- [x] Actions interdites explicitement listées par catégorie
- [x] Scénario d'erreur défini pour chaque interdiction

---

*PANAME · Contrat Système
