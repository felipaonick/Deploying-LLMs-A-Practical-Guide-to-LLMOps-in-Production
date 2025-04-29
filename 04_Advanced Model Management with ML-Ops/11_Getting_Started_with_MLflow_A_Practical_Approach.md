# 📚 Introduzione Pratica a MLflow: Loggare Parametri, Metriche, Artifacts e Modelli

---

## 🎯 Obiettivo della Lezione
- Imparare **gli strumenti base di MLflow**.
- **Configurare e usare** un server MLflow (client e server su localhost, porta 5000).
- **Organizzare e tracciare** esperimenti, run, parametri, metriche, artifacts e modelli.

---

## 🔵 Setup Iniziale
- **Prerequisito**: Avere seguito la lezione precedente e completato il setup.
- È disponibile un **notebook** nel repository, ma è **consigliato creare un file `.py` da zero** per comprendere meglio i concetti.

- **Tracking URL**:
  ```python
  mlflow.set_tracking_uri("http://localhost:5000")
  ```
  > Se client e server sono su macchine diverse, usa l'**IP esterno del server** e **apri la porta 5000** nel firewall.
  > ⚠️ Lasciare la porta aperta senza protezioni è un rischio di sicurezza (verrà risolto più avanti con l'autenticazione).

---

## 🧩 Esperimenti e Run

### 🔹 Creare un Esperimento
- Un **Esperimento** è come un **progetto** o **problema** da risolvere.
- Esempio:
  - Obiettivo: creare un modello che genera recensioni di Amazon → **Esperimento**.

  ```python
  mlflow.set_experiment("Amazon_Review_Generator")
  ```

### 🔹 Creare una Run
- Una **Run** rappresenta una **iterazione** all'interno dell'esperimento.
- Serve a tracciare modifiche di:
  - Modelli
  - Dati
  - Parametri

#### Modi per creare una Run:
- **Context Manager** (raccomandato: gestisce automaticamente chiusura):
  ```python
  with mlflow.start_run(experiment_id=experiment_id, run_name="First_try") as run:
      ...
  ```
- **Manuale** (più controllo):
  ```python
  run = mlflow.start_run(run_name="Custom_Name")
  # codice tracking
  mlflow.end_run()
  ```

- Dopo la creazione, il run appare nell'interfaccia utente (UI) di MLflow.

---

## 🧪 Tracking: Parametri, Metriche, Artifacts e Modelli

### 🔹 Parametri (`log_param`)
- **Costanti o configurazioni** di training (es: learning rate, batch size).
- Sono **key-value pairs**.

  ```python
  mlflow.log_param("learning_rate", 0.001)
  mlflow.log_param("batch_size", 32)
  mlflow.log_param("epochs", 10)
  ```

- Visualizzabili nella **UI MLflow** sotto "Parameters".

---

### 🔹 Metriche (`log_metric`)
- **Valori variabili** durante il tempo o step di training (es: loss, accuracy per epoca).
- Esempio:
  ```python
  import numpy as np

  for epoch in range(10):
      loss = np.random.random()
      accuracy = np.random.random()
      mlflow.log_metric("loss", loss, step=epoch)
      mlflow.log_metric("accuracy", accuracy, step=epoch)
  ```

- Le metriche sono graficate automaticamente in MLflow (grafici a linea).

- **Esempio creativo**: tracciare una sinusoide:
  ```python
  for x in range(100):
      mlflow.log_metric("sine_wave", np.sin(x/10), step=x)
  ```

---

### 🔹 Artifacts (`log_artifact`)
- **File di grandi dimensioni** associati alla run: datasets, modelli, log, grafici, ecc.

- Creare e loggare un file:
  ```python
  import pandas as pd

  df = pd.DataFrame(np.random.rand(10, 3), columns=["a", "b", "c"])
  df.to_csv("data/dataset.csv", index=False)
  mlflow.log_artifact("data/dataset.csv", artifact_path="data")
  ```

- Nella UI, gli artifacts appaiono come un **mini file system** dove puoi navigare e visualizzare file.

#### 🔹 Esempio avanzato: Logging di una Confusion Matrix
- Salvare una confusion matrix come file **interattivo HTML**:
  ```python
  import plotly.express as px

  fig = px.imshow(np.random.randint(0, 10, size=(3, 3)))
  fig.write_html("artifacts/confusion_matrix.html")
  mlflow.log_artifact("artifacts/confusion_matrix.html", artifact_path="artifacts")
  ```

- **Preview** possibile direttamente nella UI di MLflow.

---

### 🔹 Modelli (`log_model`)
- Loggare e salvare modelli interi.
- **Supporto nativo** per PyTorch, TensorFlow, scikit-learn, ecc.

- Esempio logging modello PyTorch:
  ```python
  import mlflow.pytorch
  import torch.nn as nn

  class DummyModel(nn.Module):
      def __init__(self):
          super(DummyModel, self).__init__()
          self.linear = nn.Linear(10, 1)

      def forward(self, x):
          return self.linear(x)

  model = DummyModel()
  mlflow.pytorch.log_model(model, artifact_path="model")
  ```

- Il modello loggato viene:
  - Impacchettato
  - Salvato con i file di dipendenze
  - Pronto per il **reload** o **serving**.

> 💬 Se hai modelli personalizzati o non supportati, la prossima lezione tratterà il **logging personalizzato**.

---

## 🔚 Chiusura della Run
- Dopo aver finito il tracking, è buona pratica **chiudere la run**:
  ```python
  mlflow.end_run()
  ```

- In MLflow UI:
  - Lo stato della run cambia in **"FINISHED"**.
  - Visualizzi parametri, metriche, artifacts e modello associati.

---

# 📋 Riepilogo della Lezione

| Elemento                  | Funzione                                              |
|-----------------------------|-------------------------------------------------------|
| **Experiment**              | Raggruppa runs relative allo stesso progetto/problema |
| **Run**                     | Iterazione o modifica sperimentale                    |
| **log_param**               | Traccia configurazioni (costanti)                     |
| **log_metric**              | Traccia performance variabili nel tempo              |
| **log_artifact**            | Salva file associati alla run                         |
| **log_model**               | Salva e versiona un intero modello                    |
| **end_run**                 | Chiude correttamente la sessione di tracking          |

---

## 📌 Cosa Fare Dopo
- Nella prossima lezione:
  - Training di un vero modello.
  - Tracking completo di parametri, metriche, artifacts e modello durante il training.

