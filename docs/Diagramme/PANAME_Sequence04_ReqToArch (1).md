# PANAME — De l'Exigence à l'Architecture
### Séquence 04 · The Missing Link

---

> **Le problème fondamental**
> Une exigence dit : *"Le système garantit X."*
> Elle ne dit jamais **qui** est responsable de X, **où** cette règle vit, **comment** elle est protégée.
>
> Ce document fait la transition :
> ```
> Exigence → Garantie → Responsabilité → Composant
> ```

---

## 4.1 — Authentification & Autorisation

---

**FR-003 · FR-004 · FR-005 · FR-006**

| | |
|---|---|
| **Nature** | Invariant de sécurité |
| **Exigence brute** | Authentification obligatoire avant toute ressource. Rôles séparés. Client ≠ Salon ≠ Admin. |
| **Garantie** | Le système garantit que chaque requête est interceptée et vérifiée avant d'atteindre n'importe quelle ressource — peu importe d'où elle vient. |
| **Logique cachée** | Le frontend peut être contourné par n'importe quel outil HTTP. La vérification ne peut pas vivre côté client. Elle doit être centrale, incontournable, et appliquée avant toute logique métier. |
| **Responsabilité** | Un seul composant intercepte toutes les requêtes et vérifie l'identité et le rôle avant de laisser passer. |
| **→ Composant** | **Gestionnaire d'Identité** |

---

**FR-007 · FR-008 · Vérification email inscription**

| | |
|---|---|
| **Nature** | Policy (règle de configuration) |
| **Exigence brute** | Réinitialisation mot de passe via email ou OTP SMS. Session invalidée après 30 jours. Vérification email après inscription. |
| **Garantie** | Le système garantit qu'aucune session ne vit indéfiniment, et qu'un utilisateur peut toujours récupérer l'accès à son compte de façon sécurisée. |
| **Logique cachée** | Ces trois règles changent ensemble quand la politique de sécurité change. Elles appartiennent au même propriétaire. La vérification email est une pré-condition à l'activation du compte — pas juste une option. |
| **Responsabilité** | Le même composant gère le cycle de vie complet des sessions et des flux de récupération d'accès. |
| **→ Composant** | **Gestionnaire d'Identité** |

---

## 4.2 — Gestion des Comptes

---

**FR-009 · FR-010 · FR-011**

| | |
|---|---|
| **Nature** | Process (capacités Client) |
| **Exigence brute** | Client modifie son profil, consulte son historique, sauvegarde des favoris. |
| **Garantie** | Le système garantit que chaque Client n'accède qu'à ses propres données — jamais à celles d'un autre. |
| **Logique cachée** | Le profil et les favoris évoluent avec le modèle Client. L'historique évolue avec le modèle Réservation. Ces responsabilités ne changent pas ensemble — elles appartiennent à des composants différents. |
| **Responsabilité** | Le profil et les favoris appartiennent au **Gestionnaire d'Identité**. L'historique appartient au **Moteur de Réservation** car c'est lui qui possède les réservations. |
| **→ Composants** | **Gestionnaire d'Identité** + **Moteur de Réservation** |

---

**FR-012 · FR-013 · FR-014 · FR-015**

| | |
|---|---|
| **Nature** | Business Rule + Invariant |
| **Exigence brute** | Admin suspend un Salon. Salon suspendu ne peut plus créer ni accepter de réservations. Toute action Admin est journalisée. |
| **Garantie** | Le système garantit que la suspension prend effet immédiatement sur toutes les capacités du Salon, et que chaque décision administrative est tracée de façon permanente et non modifiable. |
| **Logique cachée** | La suspension n'est pas un simple flag d'affichage. Elle doit être vérifiée à chaque opération du Salon — à la création d'une coiffure, à la confirmation d'un RDV. Le journal d'audit doit être append-only : s'il peut être effacé, il ne sert à rien. |
| **Responsabilité** | La suspension appartient au **Gestionnaire d'Identité**. Le journal est une responsabilité à part — il ne change jamais pour les mêmes raisons que l'auth. |
| **→ Composants** | **Gestionnaire d'Identité** + **Service de Journalisation** |

---

## 4.3 — Module de Visualisation IA

---

**FR-016 · FR-017**

| | |
|---|---|
| **Nature** | Policy (validation d'entrée) |
| **Exigence brute** | Upload limité à JPG, PNG, HEIC et 10 Mo. Tout fichier hors limites est rejeté. |
| **Garantie** | Le système garantit qu'aucun fichier non conforme n'atteint jamais le système IA externe — la validation est appliquée avant tout traitement. |
| **Logique cachée** | La validation ne peut pas être uniquement côté client — le client peut envoyer n'importe quoi directement à l'API. Elle doit être répétée côté serveur, en première ligne, avant d'engager quoi que ce soit avec le système externe. |
| **Responsabilité** | Le **Module IA** valide en entrée avant toute transmission. |
| **→ Composant** | **Module IA** |

---

**FR-019 · FR-021 · FR-022 · FR-023**

| | |
|---|---|
| **Nature** | Process (flux de génération) |
| **Exigence brute** | Sélection coiffure à superposer. Indicateur de progression. Essais multiples sans ré-upload. Téléchargement ou partage du résultat. |
| **Garantie** | Le système garantit que la photo du Client reste disponible en session active pour tous les essais successifs, et que la génération ne bloque jamais l'interface pendant le traitement. |
| **Logique cachée** | La génération peut prendre jusqu'à 15 secondes (NFR-002). Si le traitement est synchrone, l'interface gèle. Il faut un traitement asynchrone avec un mécanisme de progression découplé du résultat. La photo en session évite les ré-uploads inutiles — c'est une optimisation imposée par l'exigence. |
| **Responsabilité** | Le **Module IA** orchestre le flux complet : session photo, envoi au système externe, progression, réception du résultat, mise à disposition. |
| **→ Composant** | **Module IA** |

---

**FR-024 · FR-025**

| | |
|---|---|
| **Nature** | Invariant de vie privée |
| **Exigence brute** | Photo supprimée après 24h sans compte actif. Photo jamais utilisée sans consentement explicite. |
| **Garantie** | Le système garantit qu'aucune photo de Client ne persiste au-delà de sa durée de vie autorisée, et qu'elle n'est jamais transmise à un tiers sans accord explicite. |
| **Logique cachée** | Ces règles ne peuvent pas reposer sur une action manuelle. La suppression à 24h doit être automatique. Le consentement doit être vérifié avant chaque transmission — pas juste à l'inscription. Le stockage des fichiers est une responsabilité distincte du Module IA. |
| **Responsabilité** | Le **Module IA** vérifie le consentement avant transmission. Le **Stockage de Fichiers** applique le TTL automatiquement. |
| **→ Composants** | **Module IA** + **Stockage de Fichiers** |

---

**ER-004**

| | |
|---|---|
| **Nature** | Invariant de résilience |
| **Exigence brute** | Si le système IA est indisponible, le Client est informé. Le reste de la plateforme n'est pas bloqué. |
| **Garantie** | Le système garantit que la défaillance du système IA externe ne se propage jamais vers le Catalogue ou le Moteur de Réservation. |
| **Logique cachée** | Si le Module IA est couplé au reste du système, une panne IA rend Paname inaccessible. La dépendance externe doit être isolée derrière une frontière claire. Le Module IA doit avoir un comportement dégradé défini — il informe et s'arrête là. |
| **Responsabilité** | Le **Module IA** absorbe la panne sans la propager. |
| **→ Composant** | **Module IA** |

---

## 4.4 — Catalogue

---

**FR-026 · FR-027 · FR-028 · BR-001 · BR-002**

| | |
|---|---|
| **Nature** | Business Rules + Invariant |
| **Exigences brutes** | Salon ajoute, modifie, désactive. Coiffure liée à une réservation active non supprimable. Chaque coiffure a : photo, nom, description, prix, temps. Une coiffure appartient à exactement un Salon. Catalogue = coiffures africaines uniquement. |
| **Garantie** | Le système garantit qu'aucune coiffure référencée dans une réservation active ne peut disparaître, et qu'aucune entrée non conforme ne peut être publiée. |
| **Logique cachée** | La suppression doit interroger les réservations actives avant d'exécuter — c'est une contrainte d'intégrité référentielle, pas une règle d'interface. BR-001 implique que le Catalogue vérifie l'appartenance à un Salon unique à la création. BR-002 implique une validation du contenu à la publication. |
| **Responsabilité** | Le **Catalogue** vérifie l'intégrité référentielle, valide le contenu et applique les règles métier à chaque écriture. |
| **→ Composant** | **Catalogue** |

---

**FR-029 · FR-030 · FR-031 · FR-032 · FR-033**

| | |
|---|---|
| **Nature** | Process (lecture et filtrage) |
| **Exigences brutes** | Coiffures actives visibles. Désactivées invisibles. Filtrage par type, localisation, prix, sexe. Recherche par mots-clés. Section coiffures africaines traditionnelles. |
| **Garantie** | Le système garantit qu'un Client ne voit jamais une coiffure désactivée — quelle que soit la méthode d'accès : navigation, recherche ou filtre. |
| **Logique cachée** | Le filtre actif/inactif ne peut pas être uniquement dans l'interface. Il doit être appliqué au niveau de la requête de données. Si un Client accède directement à l'API avec l'ID d'une coiffure désactivée, le refus doit venir du Catalogue, pas de l'interface. |
| **Responsabilité** | Le **Catalogue** applique le filtre d'activation à chaque requête, indépendamment de l'origine. |
| **→ Composant** | **Catalogue** |

---

**FR-034 · FR-035 · BR-005**

| | |
|---|---|
| **Nature** | Business Rule |
| **Exigences brutes** | Client note et commente après un RDV réalisé. Client like une coiffure. Avis impossible sans RDV réalisé enregistré. |
| **Garantie** | Le système garantit qu'avant de publier un avis, l'existence d'un RDV réalisé avec ce Salon est vérifiée — jamais contournable par l'interface. |
| **Logique cachée** | Cette vérification croise deux domaines : le Catalogue (avis) et la Réservation (RDV réalisé). Elle doit se faire à l'écriture de l'avis — pas à l'affichage. Si on vérifie à l'affichage, un avis invalide peut exister en base. |
| **Responsabilité** | Le **Catalogue** vérifie auprès du **Moteur de Réservation** qu'un RDV réalisé existe avant de persister l'avis. |
| **→ Composants** | **Catalogue** + **Moteur de Réservation** |

---

## 4.5 — Vitrine Salon

---

**FR-036 · FR-037 · FR-038 · FR-039 · FR-040**

| | |
|---|---|
| **Nature** | Process (capacités Salon) |
| **Exigences brutes** | Page profil publique. Horaires et disponibilités par coiffeur. Nombre de coiffeurs et compétences. Carte interactive. Tableau de bord. |
| **Garantie** | Le système garantit que chaque Salon dispose d'une vitrine publique toujours cohérente avec son catalogue et ses disponibilités réelles. |
| **Logique cachée** | Le tableau de bord et la vitrine publique lisent les mêmes données avec des droits d'accès différents. Ils changent ensemble quand le modèle Salon change — même propriétaire. La carte interactive dépend d'un système externe de cartographie — c'est une dépendance à isoler. |
| **Responsabilité** | La **Vitrine Salon** agrège les données du Catalogue et du Moteur de Réservation. Elle délègue la géolocalisation au Service de Cartographie externe. |
| **→ Composant** | **Vitrine Salon** |

---

## 4.6 — Réservation

---

**FR-041 · FR-042 · FR-043 · FR-044**

| | |
|---|---|
| **Nature** | Invariant critique |
| **Exigences brutes** | Créneaux en temps réel. Réservation avec coiffure + coiffeur + date + heure. Disponibilité vérifiée avant confirmation. Pas deux réservations sur le même créneau pour le même coiffeur. |
| **Garantie** | Le système garantit que la vérification de disponibilité et l'écriture de la réservation sont atomiques — deux utilisateurs ne peuvent jamais obtenir le même créneau simultanément, même en cas d'accès concurrent. |
| **Logique cachée** | FR-044 révèle un problème de concurrence que l'exigence ne formule pas explicitement. "Vérifier avant d'écrire" ne suffit pas si deux requêtes arrivent en même temps — les deux passent la vérification avant que l'une n'écrive. Il faut un verrou atomique au moment de l'écriture. C'est une contrainte d'architecture, pas juste de logique. |
| **Responsabilité** | Le **Moteur de Réservation** est l'unique propriétaire. Personne d'autre ne peut écrire une réservation. Le verrou est appliqué en son sein. |
| **→ Composant** | **Moteur de Réservation** |

---

**FR-045 · FR-046 · FR-047 · NFR-016**

| | |
|---|---|
| **Nature** | Process + Invariant de résilience |
| **Exigences brutes** | Confirmation Client par SMS/email immédiatement. Rappel 24h et 2h avant. Notification Salon en temps réel. Si notification indisponible → réservation conservée, retry ultérieur. |
| **Garantie** | Le système garantit que l'indisponibilité du service de notification ne bloque jamais la création d'une réservation. La notification est un effet secondaire — jamais une condition. |
| **Logique cachée** | Si réservation et notification sont couplées, une panne de SMS empêche de réserver. NFR-016 impose le découplage. La réservation s'écrit d'abord. La notification part après, de façon asynchrone et non-bloquante. Ce découplage doit être structurel — pas juste un try/catch. |
| **Responsabilité** | Le **Moteur de Réservation** crée la réservation et publie un événement. Le **Service de Notification** consomme cet événement indépendamment. |
| **→ Composants** | **Moteur de Réservation** + **Service de Notification** |

---

**FR-048 · FR-049 · FR-050**

| | |
|---|---|
| **Nature** | Process (cycle de vie d'un RDV) |
| **Exigences brutes** | Client annule ou modifie jusqu'à 2h avant. Salon confirme, refuse ou propose un alternatif. Ticket numérique généré. |
| **Garantie** | Le système garantit que les modifications respectent la contrainte des 2h, et que chaque changement d'état produit un ticket récapitulatif à jour. |
| **Logique cachée** | Ces trois exigences font partie du même cycle de vie. Elles changent toutes quand les règles de gestion des RDV changent. Même propriétaire. |
| **Responsabilité** | Le **Moteur de Réservation** gère l'intégralité du cycle de vie d'une réservation. |
| **→ Composant** | **Moteur de Réservation** |

---

**FR-051 · FR-052 · FR-053**

| | |
|---|---|
| **Nature** | Invariant (machine d'états) |
| **Exigences brutes** | 4 états valides. Uniquement les transitions définies. Transition En attente → Réalisée interdite. |
| **Garantie** | Le système garantit qu'une réservation ne peut jamais se retrouver dans un état non défini, et que chaque transition est vérifiée avant d'être appliquée — pas après. |
| **Logique cachée** | La machine d'états ne peut pas vivre dans l'interface — elle peut être contournée par un appel direct à l'API. Elle doit être appliquée et validée au niveau de la persistance. Aucun autre composant ne peut modifier l'état d'une réservation directement. |
| **Responsabilité** | Le **Moteur de Réservation** est le seul propriétaire des transitions d'état. |
| **→ Composant** | **Moteur de Réservation** |

---

## 5 — Règles Métier (BR)

---

**BR-003**

| | |
|---|---|
| **Nature** | Business Rule (UX) |
| **Exigence brute** | La plateforme propose et suggère sans jamais imposer un choix au Client. |
| **Garantie** | Le système garantit qu'aucune fonctionnalité ne force un Client vers un Salon ou une coiffure spécifique. |
| **Logique cachée** | Ce n'est pas une règle technique — c'est une contrainte de design qui s'applique à toutes les interfaces de suggestion. Elle traverse tous les composants sans appartenir à un seul. |
| **Responsabilité** | Contrainte transversale — appliquée à chaque composant qui expose des suggestions. |
| **→ Composant** | Tous les composants · Contrainte de design |

---

**BR-004**

| | |
|---|---|
| **Nature** | Invariant |
| **Exigence brute** | Un Salon suspendu n'apparaît ni dans les résultats de recherche ni dans le catalogue. |
| **Garantie** | Le système garantit que la suspension d'un Salon efface immédiatement sa visibilité publique — pas seulement ses capacités d'action. |
| **Logique cachée** | BR-004 complète FR-013 et FR-014. La suspension a deux effets : elle retire les capacités (FR-013/014) ET la visibilité (BR-004). Ces deux effets doivent être appliqués par le même vérificateur de statut. |
| **Responsabilité** | Le **Catalogue** et la **Vitrine Salon** vérifient le statut de suspension avant d'exposer un Salon publiquement. Le **Gestionnaire d'Identité** reste la source de vérité du statut. |
| **→ Composants** | **Gestionnaire d'Identité** (source) · **Catalogue** + **Vitrine Salon** (vérificateurs) |

---

**BR-006 · BR-007**

| | |
|---|---|
| **Nature** | Invariants de sécurité |
| **Exigences brutes** | Données Client isolées des autres Clients et Salons. Admin ne modifie jamais directement le catalogue d'un Salon — il peut uniquement désactiver. |
| **Garantie** | Le système garantit que l'isolation des données est appliquée au niveau des requêtes, et que les droits de l'Admin sur le catalogue sont explicitement limités. |
| **Logique cachée** | BR-006 implique que chaque requête de données est filtrée par l'identité du demandeur — pas juste au niveau de l'interface. BR-007 implique que l'Admin n'a pas de route d'écriture sur le catalogue — uniquement une route de désactivation. |
| **Responsabilité** | Le **Gestionnaire d'Identité** applique BR-006 via le contrôle d'accès. Le **Catalogue** applique BR-007 en n'exposant pas de route de modification directe à l'Admin. |
| **→ Composants** | **Gestionnaire d'Identité** + **Catalogue** |

---

## Résultat — Les 6 composants qui émergent

> Ils ne sont pas décidés. Ils résultent du regroupement des responsabilités par cohésion.
> **Même règle du cours : "Calculating Tax" et "Generating Invoices" changent ensemble → même composant.**

| Composant | Ce qu'il porte | Exigences sources |
|---|---|---|
| **Gestionnaire d'Identité** | Auth, rôles, sessions, suspension, récupération, isolation données | FR-003 à FR-015, BR-004, BR-006 |
| **Module IA** | Upload, validation, génération, session photo, TTL, consentement, résilience | FR-016 à FR-025, ER-004 |
| **Catalogue** | Publication, filtrage, intégrité référentielle, avis, droits Admin | FR-026 à FR-035, BR-001, BR-002, BR-005, BR-007 |
| **Vitrine Salon** | Profil public, disponibilités, tableau de bord, carte | FR-036 à FR-040, BR-004 |
| **Moteur de Réservation** | Atomicité, machine d'états, cycle de vie RDV, historique Client | FR-041 à FR-053, NFR-014, NFR-015 |
| **Service de Notification** | Confirmation, rappels, découplage asynchrone, retry | FR-045, FR-046, FR-047, NFR-016 |

---
