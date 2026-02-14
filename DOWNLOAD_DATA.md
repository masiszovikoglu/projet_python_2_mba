# Guide de téléchargement des données Kaggle

## Option 1 : Téléchargement via navigateur (RECOMMANDÉ)

1. **Connectez-vous à Kaggle** (créez un compte si nécessaire) :
   https://www.kaggle.com/account/login

2. **Accédez au dataset** :
   https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets/data

3. **Cliquez sur "Download"** pour télécharger le fichier ZIP

4. **Extrayez** `transactions_data.csv` du ZIP

5. **Placez le fichier** dans le dossier `data/` de votre projet :
   ```powershell
   # Depuis le répertoire du projet
   Move-Item "C:\Users\...\Downloads\transactions_data.csv" ".\data\transactions_data.csv"
   ```

## Option 2 : Téléchargement via Kaggle API

### Installation de l'API Kaggle

```powershell
pip install kaggle
```

### Configuration des credentials

1. Allez sur https://www.kaggle.com/settings/account
2. Cliquez sur "Create New API Token"
3. Téléchargez le fichier `kaggle.json`
4. Placez-le dans : `C:\Users\<votre_nom>\.kaggle\kaggle.json`

### Téléchargement du dataset

```powershell
# Créer le dossier data s'il n'existe pas
mkdir data -ErrorAction SilentlyContinue

# Télécharger le dataset
kaggle datasets download -d computingvictor/transactions-fraud-datasets

# Extraire le fichier
Expand-Archive -Path transactions-fraud-datasets.zip -DestinationPath data -Force

# Nettoyer
Remove-Item transactions-fraud-datasets.zip
```

## Vérification

Après téléchargement, vérifiez que le fichier existe :

```powershell
# Vérifier la présence du fichier
Test-Path ".\data\transactions_data.csv"

# Afficher les premières lignes
Get-Content ".\data\transactions_data.csv" -TotalCount 5
```

Le fichier doit contenir environ **6 362 620 transactions** avec ces colonnes :
- step
- type
- amount
- nameOrig
- oldbalanceOrg
- newbalanceOrig
- nameDest
- oldbalanceDest
- newbalanceDest
- isFraud
- isFlaggedFraud

## Taille du fichier

Le fichier `transactions_data.csv` pèse environ **470 MB**.

## En cas de problème

Si le téléchargement échoue ou que le fichier est trop volumineux :

1. **Option de test** : Utilisez `sample_transactions.csv` (10 lignes) pour les tests
2. **Dataset réduit** : Créez un subset avec les premières 100 000 lignes :
   ```powershell
   Get-Content ".\data\transactions_data.csv" -TotalCount 100001 | 
     Set-Content ".\data\transactions_subset.csv"
   ```

## Important

⚠️ **Le fichier `transactions_data.csv` n'est PAS inclus dans le dépôt Git** 
(il est dans `.gitignore` car trop volumineux).

Chaque membre de l'équipe doit le télécharger individuellement.
