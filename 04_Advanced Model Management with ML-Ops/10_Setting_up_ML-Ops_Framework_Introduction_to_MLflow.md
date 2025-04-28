# 📚 Sezione: Setup Pratico — Installazione e Configurazione di un Server MLflow

---

## 🔵 Obiettivo della Lezione
In questa prima lezione pratica della sezione, l'obiettivo è **installare e configurare** tutto il necessario per ospitare un **server MLflow** personale.  
Non si scriverà codice ancora, ma si imposterà tutta l'infrastruttura di base.

---

## 📋 Materiale di Supporto
- È disponibile un **README** allegato alla lezione:
  - Contiene **comandi**, **spiegazioni extra** e **istruzioni dettagliate**.
  - **Consigliato** consultarlo per seguire meglio il setup.

---

## 🛠️ Passaggi per il Setup del Server MLflow

### 1. **Creazione di un Utente Dedicato**
- **Utente creato**: `mlflow`
- **Motivazione**:
  - Migliore **organizzazione**.
  - Minore **propensione agli errori**.
- **Password**:
  - **Raccomandato** scegliere una password **sicura**.
- **Permessi**:
  - È stato aggiunto al gruppo **sudoers** *(opzionale ma utile per i permessi elevati)*.
  - **Nota**: In contesti di produzione, si consiglia di evitare privilegi sudo per motivi di **sicurezza**.

---

### 2. **Preparazione dell'Ambiente Python**
- **Requisiti**:
  - **Python 3**.
  - **Virtualenv**.
- **Nota**:
  - Probabilmente già presenti su molte macchine.
  - Comandi per l’installazione su Ubuntu presenti nel **README**.

- **Motivazione per usare un Virtualenv**:
  - **Isolamento dell'ambiente**.
  - **Evitare conflitti** tra pacchetti Python.
  - **Facilità di manutenzione** futura.

---

### 3. **Creazione della Directory di Lavoro**
- Directory principale: `mlflow_server`
- All'interno:
  - Creazione dell'ambiente virtuale.
  - Salvataggio di tutti i file e configurazioni necessari.

---

### 4. **Installazione di MLflow**
- **Versione consigliata**: `2.7.1`
  - **Motivazione**:
    - Coerenza con il materiale del corso.
    - Evitare problemi di compatibilità dovuti all'evoluzione rapida della libreria.
- **Alternativa**:
  - Si può usare l'ultima versione disponibile, ma potrebbero esserci **piccole differenze**.

---

### 5. **Configurazione dei Backend di Storage**

#### a) **Backend per Metriche e Parametri**
- **Database scelto**: `SQLite` (per test e uso individuale).
- **Altre opzioni**:
  - `MySQL` (consigliato per uso **multiutente** o **team**).
- **Nota**:
  - I dettagli per entrambe le opzioni sono disponibili nel **README**.

#### b) **Backend per gli Artifacts**
- **Archiviazione scelta**: **Storage locale** (inizialmente).
  - Archivia modelli, file di dati e altri artifacts di grandi dimensioni.
- **Soluzioni consigliate per produzione**:
  - **S3** (Amazon o tramite **MinIO**).
  - **HDFS** (per esigenze aziendali più avanzate).

---

### 6. **Avvio del Server MLflow**
- Il comando di avvio è disponibile nel **README**.
- Configurazione base:
  - **Database URI** → punta al file SQLite creato.
  - **Artifact URI** → punta alla directory locale designata.

- **Porta di default**: `5000`
  - MLflow sarà raggiungibile su `localhost:5000`.

---

### 7. **Accesso Locale o Remoto**

| Tipo di Installazione          | Azione Necessaria     |
|:--------------------------------|:-----------------------|
| Installazione Locale            | Nessuna: aprire direttamente `localhost:5000` nel browser. |
| Installazione Remota            | **Creare un tunnel SSH** per inoltrare la porta `5000`. |

- **Creazione Tunnel SSH**:
  ```bash
  ssh -L 5000:localhost:5000 user@remote_machine_ip
  ```
- Dopo il tunneling:
  - Accedere da browser locale a `localhost:5000`.

---

## 📸 Risultato Finale

- Apertura dell'interfaccia MLflow su `localhost:5000`.
- Server attivo e funzionante!
- Al momento l'interfaccia sarà **vuota**, ma verrà popolata nelle prossime lezioni quando si caricheranno i primi esperimenti e modelli.

---

## 🎯 Riepilogo dei Passi Effettuati

1. Creato utente `mlflow`.
2. Installato Python 3, virtualenv.
3. Creato ambiente virtuale isolato.
4. Installato MLflow versione 2.7.1.
5. Configurati storage backend (SQLite e file system locale).
6. Avviato server MLflow sulla porta 5000.
7. Creato tunnel SSH per accesso remoto (se necessario).
8. Confermato l'accesso all'interfaccia web.

---

## 🚀 Prossimi Passi
Nella prossima lezione:
- **Utilizzeremo l’interfaccia MLflow**.
- **Caricheremo dati** e **monitoreremo esperimenti reali**.
- **Esploreremo le funzionalità** offerte dal framework.