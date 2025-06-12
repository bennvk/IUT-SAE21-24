## 📊 Planning Gantt – Projet Pépinière (SAE21 & SAE24)

### 📌 Contexte

Ce projet est réalisé dans le cadre du **BUT R&T – IUT de Béthune**, pour les SAE21 (Réseaux) et SAE24 (Intégration). Il consiste à concevoir et déployer l'infrastructure réseau, téléphonique et les services numériques d’une entreprise fictive située dans une **pépinière d’entreprises**.  
Le projet est mené par **la société 11**, membre de la pépinière.

---

### 🎯 Objectifs du projet

- Concevoir un **plan d'infrastructure complet** (réseau, services, sécurité, accès distants)
- Déployer et configurer des **équipements réseau (Cisco)** et des **services virtualisés (Docker)**
- Mettre en place une **infrastructure téléphonique IP** priorisée
- Superviser la température via **LoRaWAN**
- Traiter des **flux vidéos (caméras IP)** et développer une **reconnaissance automatisée**
- Réaliser une **analyse de sécurité réseau** et une **interception VoIP**
- Organiser le travail en équipe avec **RACI**, **Gantt** et **journal de bord**

---

### 👥 Société 9 – Équipe projet

- [Mathéo Crepieux]
- [Raphaël Laurent]
- [Benjamin Petillon]
- [Alan Gaubert]
- [Alexis Stingre]
  
---

### 🗓️ Planning Gantt (prévisionnel)

Le projet se déroule sur **6 jours** en équipe, précédés d'une journée de préparation.  
Le diagramme de Gantt ci-dessous présente les grandes étapes du projet, leur durée estimée, ainsi que les interdépendances critiques.

| **Tâche**                                   | **Durée** | **Début** | **Fin**   | **Dépendances**                  |
|--------------------------------------------|-----------|-----------|-----------|----------------------------------|
| Réunion de lancement / plan individuel     | 0.5 j     | J1 AM     | J1 AM     | -                                |
| Plan commun + Matrice RACI + Gantt         | 0.5 j     | J1 PM     | J1 PM     | Réunion de lancement             |
| Recherche documentation                    | 1 j       | J1 PM     | J2 AM     | -                                |
| Câblage et topologie réseau                | 1 j       | J2        | J3        | Plan réseau finalisé             |
| Config routeurs / switchs                  | 1 j       | J3        | J4        | Câblage terminé                  |
| Installation des serveurs (Docker)         | 1 j       | J3        | J4        | Plan services validé             |
| Installation des clients (Linux/Win/macOS) | 0.5 j     | J4 AM     | J4 AM     | Réseau fonctionnel               |
| Configuration des services réseau          | 1 j       | J4        | J5        | Serveurs opérationnels           |
| Mise en place téléphonie IP                | 0.5 j     | J5 AM     | J5 AM     | Réseau + IPBX dispo              |
| Priorisation QoS téléphonie                | 0.5 j     | J5 PM     | J5 PM     | Téléphonie configurée            |
| Capteur température LoRa                   | 0.5 j     | J5 PM     | J6 AM     | Serveur web + réseau LoRa       |
| Analyse réseau LoRa (maths)                | 0.5 j     | J6 AM     | J6 AM     | Capteur LoRa en place            |
| Script traitement image (caméras IP)       | 0.5 j     | J5 PM     | J6 AM     | Caméras installées               |
| Script interception VoIP                   | 0.5 j     | J6 AM     | J6 PM     | Capture de trames                |
| Rapport final + Archivage                  | 0.5 j     | J6 PM     | J6 PM     | Toutes les tâches terminées      |
| Soutenance orale                           | 0.5 j     | J7        | J7        | Rapport et arch. déposés         |
