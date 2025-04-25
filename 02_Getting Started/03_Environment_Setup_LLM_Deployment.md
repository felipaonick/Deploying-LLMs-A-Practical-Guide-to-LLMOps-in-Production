# 🛠️ Setup dell'Ambiente: Come prepararsi e usare al meglio le risorse del corso

> Traduzione e rielaborazione in italiano della terza lezione  
> 📅 Data generazione: 2025-03-22

---

## 👋 Benvenuto di nuovo!

Poiché questo è un **corso molto pratico**, è importante configurare correttamente l’ambiente di sviluppo per scrivere e testare codice in modo efficiente.

> ⏭️ Se preferisci iniziare subito con la teoria, puoi **saltare momentaneamente questa lezione** e tornare in seguito.  
> Il primo esercizio pratico sarà nella **Sezione 4**, quindi hai ancora un po’ di tempo prima di iniziare a programmare.

---

## 💻 Editor consigliato: VS Code

Se hai già un editor in cui ti trovi bene a scrivere codice Python, puoi continuare a usarlo.  
Altrimenti, ti consiglio di usare **Visual Studio Code (VSCode)**:

- ✅ Gratuito, leggero, open source
- ⚙️ Ottimo supporto per Python e workflow interattivi
- 🌐 Perfetto per lavorare anche su **macchine remote**

### 🔌 Estensioni necessarie:
1. **Python Extension** – per scrivere ed eseguire codice Python
2. **Jupyter Extension** – per lavorare con notebook interattivi

### ▶️ Modalità Interattiva:
- Permette di **eseguire codice riga per riga**, vedere risultati in tempo reale, e sperimentare in modo ordinato.
- Per abilitarla:
  - Premi `Ctrl + Shift + P` (o `Cmd + Shift + P` su Mac)
  - Cerca `Send to Interactive`
  - Attiva la funzione

---

## 📒 Jupyter Notebook & Google Colab

Alcune lezioni includono **notebook Jupyter** già pronti all’uso:

- ✅ Puoi aprirli su **Google Colaboratory** per iniziare subito
- ⚠️ Tuttavia, per lezioni più avanzate con setup di sistema e comunicazioni tra servizi, **Colab non basta**
- Usa Colab solo per capire la **logica di base**

---

## 🖥️ Uso della GPU

Alcune lezioni prevedono l’uso di **GPU per training o inferenza**.

- Se hai una GPU locale, perfetto!
- Se usi Colab:
  - Vai su `Runtime > Change runtime type`
  - Seleziona **GPU**

---

## 🧰 Setup di sistema e server

Per il setup di server, code tracker e code queue, useremo principalmente **Ubuntu** come sistema operativo.

- Le istruzioni sono simili anche per altri OS
- Tuttavia, **la compatibilità completa è garantita solo su Ubuntu**

---

## 🌐 Lavorare da remoto (opzionale)

Se utilizzi una macchina **remota o cloud** (es. una VM):

- Installa l’estensione **Remote - SSH** in VS Code
- Modifica il file `config` SSH con l’IP del server
- Collega la macchina remota da **in basso a sinistra in VSCode**

---

## 🧪 Deployment distribuito finale

Nella **sezione finale** faremo un deployment distribuito su un **cluster di più macchine**.

- L’ideale sarebbe avere **almeno due server** separati
- ❗ Se non è possibile, puoi seguire comunque quasi tutti i passaggi su **una singola macchina**
- L’importante è **comprendere bene i concetti e le pratiche**

---

## 📁 Risorse del corso

Per ogni lezione pratica troverai:
- Codice sorgente
- Notebook
- Script di setup
- Link utili

> 🔎 Verifica sempre la **scheda “Risorse”** accanto ai video delle lezioni!

---

## ✅ Tutto pronto!

Hai completato il setup necessario!  
Ora possiamo tornare al corso e iniziare a esplorare il mondo pratico dei LLM.

Grazie, e ci vediamo nella prossima lezione!
