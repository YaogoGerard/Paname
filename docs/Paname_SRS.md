# PANAME — Software Requirements Specification (SRS)

---

## 1. Introduction

Ce document définit les exigences formelles, vérifiables et indépendantes de toute implémentation du système Paname.

Il spécifie ce que le système **MUST** faire et ce qu'il **MUST NOT** faire, sans décrire comment ces comportements sont implémentés.

---

## 2. Périmètre du système

Paname (« Coiffer » en mooré) est une plateforme numérique de mise en relation entre clients et salons de coiffure africains locaux.

Le système repose sur trois piliers fonctionnels :

- **Visualiser** — module de try-on virtuel IA : le client uploade sa photo et essaie des coiffures virtuellement.
- **Choisir** — catalogue de coiffures africaines géré par les salons, consultable et filtrable.
- **Réserver** — prise de rendez-vous en ligne avec gestion des disponibilités en temps réel.

### Hors périmètre (v1)

- Paiement en ligne
- Application mobile native
- Messagerie interne Client–Salon
- Soins autres que la coiffure
- Programme de fidélité

---

## 3. Acteurs

### 3.1 Acteurs humains

- **Client** — explore le catalogue, utilise la visualisation IA, réserve un créneau.
- **Salon / Coiffeur** — gère son profil, publie son catalogue, confirme les réservations.
- **Administrateur** — modère le contenu, gère les comptes, consulte les logs.

### 3.2 Systèmes externes

- **Système IA générative** — génère les aperçus coiffure sur photo.
- **Service de notification** — envoi de SMS / email pour confirmations et rappels.

---

## 4. Exigences fonctionnelles

### 4.1 Authentification & Autorisation

FR-001: Le Système MUST permettre à un utilisateur de s'inscrire en tant que Client, avec : nom, prénom, numéro de téléphone et sexe.

FR-002: Le Système MUST permettre à un utilisateur de s'inscrire en tant que Salon, avec : nom du salon, localisation, description et spécialités.

FR-003: Le Système MUST authentifier tout utilisateur avant de lui donner accès à une ressource protégée.

FR-004: Le Système MUST appliquer un contrôle d'accès basé sur les rôles (Client, Salon, Administrateur).

FR-005: Un Client MUST NOT accéder aux interfaces de gestion réservées aux Salons ou aux Administrateurs.

FR-006: Un Salon MUST NOT accéder aux données d'un autre Salon.

FR-007: Le Système MUST permettre la réinitialisation du mot de passe via email ou OTP SMS.

FR-008: Le Système MUST invalider la session après 30 jours d'inactivité.
 
 
        Le Système MUST faire une verification par mail apresson inscription



---

### 4.2 Gestion des comptes utilisateurs

FR-009: Le Système MUST permettre à un Client de consulter et modifier son profil (nom, prénom, téléphone, sexe).

FR-010: Le Système MUST permettre à un Client de consulter l'historique de ses réservations passées et à venir.

FR-011: Le Système MUST permettre à un Client de sauvegarder des coiffures en favoris.

FR-012: Le Système MUST permettre à un Administrateur de suspendre un compte Salon.

FR-013: Un Salon suspendu MUST NOT créer de nouvelles entrées dans le catalogue.

FR-014: Un Salon suspendu MUST NOT accepter de nouvelles réservations.

FR-015: Le Système MUST journaliser toute action administrative (suspension, suppression de contenu).

---

### 4.3 Module de visualisation IA 

FR-016: Le Système MUST permettre à un Client d'uploader une photo de son visage (formats : JPG, PNG, HEIC ; taille max : 10 Mo).

FR-017: Le Système MUST rejeter tout fichier dont le format ou la taille dépasse les limites définies en FR-016.

FR-018: Le Système MUST détecter automatiquement le sexe, la couleur des cheveux et la forme du visage à partir de la photo uploadée.(optionnel)

FR-019: Le Système MUST permettre au Client de sélectionner une coiffure du catalogue pour la superposer sur sa photo.

FR-021: Le Système MUST afficher un indicateur de progression pendant la génération de l'image.

FR-022: Le Système MUST permettre au Client d'essayer plusieurs coiffures successivement sans ré-uploader sa photo.

FR-023: Le Système MUST permettre au Client de télécharger ou partager l'image générée.

FR-024: Le Système MUST NOT stocker la photo du Client au-delà de 24h si elle n'est pas associée à un compte actif.

FR-025: Le Système MUST NOT utiliser la photo d'un Client à d'autres fins que la génération IA sans consentement explicite.

---

### 4.4 Catalogue de coiffures africaines

FR-026: Le Système MUST permettre à un Salon d'ajouter, modifier et désactiver des coiffures dans le catalogue.

FR-027: Le Système MUST NOT permettre la suppression d'une coiffure associée à une réservation active.

FR-028: Chaque entrée du catalogue MUST contenir : photo(s), nom, description, prix indicatif, temps de réalisation estimé.

FR-029: Le Système MUST afficher l'ensemble des coiffures actives aux Clients.

FR-030: Le Système MUST NOT afficher les coiffures désactivées aux Clients.

FR-031: Le Système MUST permettre aux Clients de filtrer le catalogue par : type de coiffure, localisation, fourchette de prix, sexe.

FR-032: Le Système MUST permettre aux Clients de rechercher une coiffure par mots-clés.

FR-033: Le Système MUST inclure une section dédiée mettant en avant les coiffures africaines traditionnelles (tresses, locks, twists, afros, nattages…).

FR-034: Le Système MUST permettre aux Clients de noter et commenter une coiffure après un RDV réalisé.

FR-035: Le Système MUST permettre aux Clients de liker une coiffure, le compteur étant visible de tous.
        Le catalogue MUST BE à etre liker et commenter

### 4.5 Vitrine numérique du Salon

FR-036: Le Système MUST générer une page profil publique pour chaque Salon, affichant : nom, photos, localisation, description, spécialités, horaires, avis et catalogue.

FR-037: Le Système MUST permettre à un Salon de configurer ses horaires d'ouverture et ses disponibilités par coiffeur.

FR-038: Le Système MUST permettre à un Salon de configurer le nombre de coiffeurs disponibles et les coiffures qu'ils maîtrisent.

FR-039: Le Système MUST permettre aux Clients de localiser les Salons sur une carte géographique interactive.

FR-040: Le Système MUST fournir au Salon un tableau de bord affichant : nombre de RDV, coiffures les plus demandées, avis reçus, nombre de vues du profil.

---

### 4.6 Système de réservation en ligne

FR-041: Le Système MUST afficher en temps réel les créneaux disponibles d'un Salon.

FR-042: Le Système MUST permettre à un Client de réserver un créneau en sélectionnant : coiffure souhaitée, coiffeur (optionnel), date et heure.

FR-043: Le Système MUST valider la disponibilité du créneau avant de confirmer la réservation.

FR-044: Le Système MUST NOT autoriser deux réservations sur le même créneau pour le même coiffeur.

FR-045: Le Système MUST envoyer une confirmation de réservation au Client par SMS et/ou email immédiatement après la réservation.

FR-046: Le Système MUST envoyer un rappel automatique au Client 24h et 2h avant le rendez-vous.

FR-047: Le Système MUST notifier le Salon en temps réel lors d'une nouvelle réservation.

FR-048: Le Système MUST permettre au Client d'annuler ou modifier un RDV jusqu'à 2h avant l'heure prévue.

FR-049: Le Système MUST permettre au Salon de confirmer, refuser ou proposer un créneau alternatif.

FR-050: Le Système MUST générer un ticket numérique récapitulatif du RDV (coiffure, salon, date, heure, coiffeur).

FR-051: Le Système MUST prendre en charge les états suivants pour une réservation :
- En attente
- Confirmée
- Annulée
- Réalisée

FR-052: Le Système MUST appliquer uniquement les transitions d'état valides définies en Section 6.

FR-053: Une réservation MUST NOT passer directement de l'état En attente à l'état Réalisée.

---

## 5. Règles métier

BR-001: Une coiffure MUST appartenir à exactement un Salon.

BR-002: Le catalogue MUST uniquement contenir des coiffures africaines — aucun autre type de prestation n'est inclus.

BR-003: La plateforme MUST proposer et suggérer des coiffures et salons, sans jamais imposer un choix au Client.

BR-004: Un Salon suspendu MUST NOT apparaître dans les résultats de recherche ni dans le catalogue.

BR-005: Un avis Client MUST NOT être publié sans qu'un RDV Réalisé avec ce Salon soit enregistré dans le Système.

BR-006: Les données personnelles d'un Client MUST rester isolées et inaccessibles aux autres Clients et Salons.

BR-007: Un Administrateur MUST NOT modifier directement le contenu du catalogue d'un Salon — il peut uniquement le désactiver.

---

## 6. Exigences non-fonctionnelles

### 6.1 Performance

NFR-001: Le Système MUST répondre aux requêtes API standard en moins de 2 secondes sous charge normale.

NFR-002: Le Système MUST générer l'aperçu IA en moins de 15 secondes dans des conditions normales.

NFR-003: Le Système MUST afficher les pages principales en moins de 3 secondes sur une connexion 3G.

NFR-004: Le Système MUST supporter au moins 1 000 utilisateurs actifs simultanés sans dégradation des fonctionnalités cœur.

NFR-005: Le Système MUST garantir une disponibilité mensuelle supérieure ou égale à 99%.

---

### 6.2 Sécurité

NFR-006: Le Système MUST chiffrer toutes les communications Client–Serveur via HTTPS / TLS 1.2 minimum.

NFR-007: Le Système MUST NOT stocker les mots de passe en clair — ils MUST être hashés (bcrypt ou Argon2).

NFR-008: Le Système MUST journaliser toutes les tentatives d'authentification (réussies et échouées).

NFR-009: Le Système MUST implémenter une protection contre les attaques CSRF, XSS et injections SQL.

NFR-010: Toute ressource protégée MUST exiger une authentification valide avant d'être accessible.

---

### 6.3 Accessibilité & Compatibilité

NFR-011: Le Système MUST être utilisable sur mobile (iOS 14+ et Android 8+) et desktop via interface web responsive.

NFR-012: Le Système MUST être compatible avec Chrome, Firefox, Safari et Edge (2 dernières versions majeures).

NFR-013: Le Système MUST respecter les critères d'accessibilité WCAG 2.1 niveau AA.

---

### 6.4 Fiabilité & Intégrité

NFR-014: Le Système MUST préserver l'intégrité des données de réservation en cas d'arrêt inattendu.

NFR-015: Si une erreur interne survient lors de la création d'une réservation, le Système MUST annuler les opérations partielles (rollback).

NFR-016: Si le service de notification est indisponible, le Système MUST conserver la réservation et réessayer l'envoi ultérieurement.

---

### 6.5 Conformité légale

NFR-017: Le Système MUST permettre à tout utilisateur de demander la suppression de son compte et de ses données personnelles.

NFR-018: La collecte et le traitement des données personnelles MUST être conformes au RGPD ou à la législation locale applicable.

---

## 7. Exigences de gestion des erreurs

ER-001: Le Système MUST retourner une erreur explicite si le fichier photo uploadé dépasse la taille ou le format autorisé.

ER-002: Le Système MUST retourner une erreur explicite si le créneau sélectionné n'est plus disponible au moment de la confirmation.

ER-003: Le Système MUST retourner une erreur d'autorisation lorsqu'un acteur tente d'accéder à une ressource non autorisée.

ER-004: Si le service d'IA générative est indisponible, le Système MUST en informer le Client et MUST NOT bloquer l'accès au reste de la plateforme.

ER-005: Le Système MUST rejeter toute entrée malformée ou incomplète et retourner un message d'erreur descriptif.

ER-006: Le Système MUST NOT exposer de détails techniques d'implémentation dans les messages d'erreur retournés aux utilisateurs.

---

## 8. Machine d'états — Réservation

Le Système MUST enforcer exclusivement les transitions d'état suivantes :

| État source  | État cible   | Condition / Acteur déclencheur                          |
|--------------|--------------|---------------------------------------------------------|
| En attente   | Confirmée    | Le Salon confirme la réservation                        |
| En attente   | Annulée      | Le Client annule (> 2h avant) ou le Salon refuse        |
| Confirmée    | Annulée      | Le Client annule (> 2h avant le RDV)                    |
| Confirmée    | Réalisée     | Le RDV a eu lieu — le Salon marque comme réalisé        |
| En attente   | ~~Réalisée~~ | **INTERDIT** — voir FR-053                              |

---

## 9. Critères de conformité

Le système sera considéré conforme à ce SRS lorsque :

- Toutes les exigences **MUST** sont validées par des tests automatisés ou manuels documentés.
- Toutes les exigences **MUST NOT** ont des tests négatifs prouvant leur application.
- Toutes les transitions d'état de la réservation sont vérifiables et testées.
- Toutes les règles de contrôle d'accès sont vérifiables et appliquées sans exception.
- Les critères de performance (NFR-001 à NFR-005) sont mesurés et atteints en conditions de charge réelle.

---

## 10. Clause d'indépendance d'implémentation

Ce document ne prescrit pas :

- Le langage de programmation utilisé.
- Le moteur de base de données.
- Le framework frontend ou backend.
- Le modèle d'IA générative spécifique utilisé.
- Le modèle de déploiement (cloud, on-premise, serverless…).

Toutes les exigences sont indépendantes des choix technologiques et s'appliquent quelle que soit l'architecture retenue.

---

*Fin du document — PANAME SRS v2.0 · 53 exigences formelles*
