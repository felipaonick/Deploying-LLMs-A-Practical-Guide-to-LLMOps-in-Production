# 📚 Lezione Pratica: Training Avanzato e Tracking con MLflow

---

## 🔵 Obiettivo della Lezione
In questa lezione:
- Alleniamo un **modello Transformer** (DistilBERT) su un dataset di classificazione di news.
- Integriamo **MLflow Tracking** per monitorare parametri, metriche, dati e modelli.
- Impariamo a **loggare**, **salvare** e **registrare** un modello su MLflow.

---

## 🛠️ Setup Iniziale

1. **Creazione Configurazione di Training**
   - Definito un dizionario `config` con:
     - Learning Rate
     - Batch Size
     - Numero di Epochs
     - Tipo di Task (`classification`)
     - Frequenza di logging (ogni 100 step)
     - Lunghezza massima input
     - Percorsi per output e checkpoint

2. **Connessione a MLflow Server**
   - Connessione manuale tramite `mlflow.set_tracking_uri()`.
   - Creazione esperimento `sequence_classification`.
   - Avvio del primo **Run** chiamato ad esempio `distilbert_agnews`.

---

## 📦 Tracking Parametri e Dati

- **Logging parametri**:
  - Tutti i parametri di `config` sono loggati con `mlflow.log_params(config)`.
  
- **Preprocessing Dataset**:
  - Dataset scelto: **AG News** (classificazione in 4 categorie).
  - Campionamento: **20.000 esempi** per velocizzare il training.
  - **Tokenizzazione**:
    - Uso del tokenizer di DistilBERT (`DistilBertTokenizerFast`).
    - Implementata funzione custom di tokenizzazione.
    - Padding e Truncation abilitati.
  
- **Salvataggio dataset**:
  - Salvato in locale come file `.parquet`.
  - **Logging dei dataset**:
    - Entrambi i file (training e test) loggati come artifacts su MLflow.

---

## 🏋️‍♂️ Training Pipeline

- **DataLoader**:
  - Preparati `DataLoader` per train e test set.
  - Utilizzate le colonne: `input_ids`, `attention_mask`, `labels`.

- **Modello**:
  - Caricato modello `DistilBERTForSequenceClassification`.
  - Impostati parametri dal `config` (es. learning rate, output_dir).

- **Ottimizzatore**:
  - AdamW con learning rate definito.

- **Funzione di Valutazione**:
  - Implementata funzione di evaluation personalizzata:
    - Calcolo di: **Accuracy**, **F1**, **Precision**, **Recall**.
    - Uso di `sklearn.metrics`.

- **Training Loop**:
  - Standard:
    - Forward pass
    - Calcolo della loss
    - Backward pass
    - Aggiornamento pesi
  - **Logging della loss** ogni 100 step.
  - **Logging metriche di validazione** dopo ogni epoch.

- **Progress Bar**:
  - Usato `Tqdm` per migliorare l'esperienza visiva durante il training.

---

## 📈 Risultati del Tracking su MLflow

- **Metriche**:
  - Loss tracciata ogni 100 step.
  - Accuracy, F1, Precision, Recall tracciate alla fine di ogni epoch.
  - Metrics associate a step specifici (timeline chiara).

- **Artifacts**:
  - Datasets salvati.
  - Modello e Tokenizer salvati manualmente nella cartella di output.

---

## 📦 Salvataggio e Registrazione del Modello

1. **Salvataggio manuale**:
   - Salvataggio del modello (`save_pretrained`) e del tokenizer in locale.

2. **Logging come Artifact**:
   - Caricamento dell’intera directory come **artifact** in MLflow.

3. **Registrazione come Modello MLflow**:
   - Usato `mlflow.register_model()`:
     - Specificato `artifact_path` e `model_name`.
   - Ora disponibile nella **Model Registry**:
     - Versionamento
     - Staging (es. "Production", "Staging", "Archived")
     - Integrazione con altre pipeline di MLOps.

---

## ✅ Riepilogo delle Attività Eseguite

| Attività | Stato |
|:---------|:------|
| Definito esperimento MLflow | ✅ |
| Tracciati parametri di training | ✅ |
| Tracciati datasets come artifacts | ✅ |
| Loggate metriche durante il training | ✅ |
| Salvataggio modello finale | ✅ |
| Registrazione modello nella Model Registry | ✅ |

---

## 🎯 Cosa abbiamo imparato

- Come **integrare MLflow** in un pipeline di training.
- Importanza di **tracciare ogni componente** (parametri, dati, metriche, modelli).
- Come **salvare** un modello e **gestirlo** tramite la **Model Registry**.
- Il valore pratico del **monitoraggio real-time** durante il training.

---

## 🚀 Prossimi Passi
Nella prossima lezione:
- Impareremo a **servire** i modelli registrati tramite MLflow.
- Vedremo **versionamento**, **staging** e **deployment** automatico.
