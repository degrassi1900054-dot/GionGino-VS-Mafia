# GionGino-VS-Mafia


---

<div align="center">
  <a href="https://github.com/degrassi1900054-dot/GionGino-VS-Mafia"><img src="https://img.shields.io/badge/GitHub-Repo-blue?style=for-the-badge&logo=github"></a>

  <a href="https://discord.com/channels/1504894467319271545/1504896923012960369"><img src="https://img.shields.io/badge/Discord-Server-purple?style=for-the-badge&logo=discord"></a>
 
  <a href="https://tel.meet/biq-nrqj-adn?pin=1527822034426"><img src="https://img.shields.io/badge/Meet-Server-red?style=for-the-badge&logo=google"></a>
</div>


---

## 1. Trama gioco
### L'Inizio: La Chiamata della Nonna - O' rre cumanna e o' vecchio cunsiglia.

1946. John Gino vive a New York da dieci anni. Agli occhi di tutti è solo un immigrato tranquillo, ma dentro di sé nasconde i fantasmi di un passato violento a Napoli. Se n'era andato perché "si era rotto o cazz" di quella vita, dei tradimenti e del sangue, cercando un futuro pulito.

Un giorno riceve la chiamata della nonna. La vecchia non gli chiede di tornare per vendetta o per soldi, ma per una vergogna intollerabile. A Napoli la pizza non viene più cucinata secondo la tradizione napoletana, le pizzerie sono gestite dai mafiosi che fanno delle pizze disgustose a prezzi altissimi. Napoli non è più la capitale della pizza.

Questo tocca l'unico briciolo di orgoglio e rispetto che a John è rimasto. Nella sua testa scatta qualcosa: puoi uccidere, puoi rubare, ma non puoi toccare la pizza. Decide di imbarcarsi sul primo piroscafo per l'Italia e far ritornare le pizzerie di Napoli a fare le pizze migliori del mondo. Per raggiungere il suo obbiettivo deve affrontare i boss della malavita Napoletana che un tempo lui chiamava famiglia.

### La Campagna di Napoli: Un "Metodo" Particolare

John torna a Napoli e inizia la sua crociata. John Gino scende dalla nave con la sua valigia, l'aria anni '40 è pesante, ma ad attenderlo al varco non ci sono i doganieri, bensì gli scagnozzi del clan dove effettuare la sua prima uccisione dopo anni e mettersi alla ricerca dei vari mini boss della malavita napoletana. Sa esattamente come muoversi nei vicoli, conosce i punti deboli del clan e sa come far parlare la gente.

### Il Finale

John smantella i clan minori e arriva finalmente al vertice. Viene condotto al cospetto del Boss Finale, l'uomo d'ombra che ha unito tutte le famiglie e ha trasformato la pizza in un business multimilionario di fango e gesso. Il Boss si gira.

È un uomo potente, con un nome altisonante da capoclan. Ma John lo riconosce all'istante: è il suo vecchio compagno di batteria di dieci anni prima, l'uomo con cui divideva le rapine e i marciapiedi prima di fuggire in America, ai vecchi tempi erano come fratelli. In questi dieci anni, "nome Boss" ha scalato la piramide ed è diventato il Leader Supremo della camorra, cambiando nome per proteggere la sua identità. Anche il Boss lo riconosce immediatamente e, con sua grande sorpresa, scopre che colui che ha sempre considerato un fratello, parte della famiglia, deve ora essere eliminato per mantenere in piedi il suo impero.

---

## 2. Struttura Architetturale
├── Core Systems

├── Gameplay Systems

├── Audio Systems

├── Narrative Systems

├── Art & Assets

├── UI

└── Tools & Data

---

## 3. Core system


---

## 4. Gameplay System

---

## 5. Audio Systems

---

## 6. Narrative Systems

I file che gestiscono i dialoghi all'interno del gioco sono in formato **`.txt`** e seguono una struttura logica precisa per facilitarne la gestione e l'implementazione nei vari livelli.

### Regole di Formattazione del Testo
Per garantire la corretta lettura da parte del sistema di parsing, tutti i testi all'interno dei file devono rispettare le seguenti regole:
* **Case Sensitivity:** Tutti i dialoghi devono essere scritti interamente in **minuscolo**.
* **Sintassi:** Ogni singola battuta o testo del dialogo deve essere sempre racchiuso tra virgolette doppie (`""`).

### Struttura e Naming Convention dei File

* **Dialoghi di Livello:** La maggior parte dei dialoghi è suddivisa per livello. Ogni livello possiede un dialogo introduttivo.
    * *Naming:* `iniziox.txt` (dove `x` rappresenta il numero del livello, es. `inizio1.txt`, `inizio2.txt`).
* **Dialoghi dei Boss:** I dialoghi relativi agli scontri con i boss sono separati in file specifici che portano il nome del boss stesso. Per ogni boss sono previsti due file distinti:
    * **Prima dello scontro:** `[nome_boss]_inizio.txt` (es. `tony_montana_inizio.txt`).
    * **Dopo la sconfitta del boss:** `[nome_boss]_fine.txt` (es. `tony_montana_fine.txt`, attivato quando John sconfigge il boss).

### Eccezioni

* 👵 **Nonna e John Gino:** Il dialogo tra la nonna e John Gino fa eccezione alla divisione standard per livelli: non è associato a un livello specifico ed è gestito in un file `.txt` completamente separato e dedicato.
* 🚫 **Livello 4 (Nessun Boss):** Il livello 4 rappresenta un'eccezione in quanto non prevede alcuno scontro con un boss. Di conseguenza, al posto dei file del boss, è presente un dialogo di conclusione livello nominato `fine4.txt`.

---

### Tabella Riassuntiva dei File dialogue

| Tipo di Dialogo | Naming Convention / File | Formato Testo | Descrizione |
| :--- | :--- | :--- | :--- |
| **Inizio Livello** | `iniziox.txt` | Minuscolo tra `""` | Dialogo introduttivo all'avvio del livello `x`. |
| **Fine Livello (Solo Lvl 4)** | `fine4.txt` | Minuscolo tra `""` | Dialogo di conclusione specifico per il livello 4 (senza boss). |
| **Pre-Boss** | `[nome_boss]_inizio.txt` | Minuscolo tra `""` | Dialogo cinematico che precede lo scontro con il boss. |
| **Post-Boss** | `[nome_boss]_fine.txt` | Minuscolo tra `""` | Dialogo che si attiva non appena John sconfigge il boss. |
| **Speciale** | File dedicato Nonna-John | Minuscolo tra `""` | Dialogo unico tra la nonna e John Gino, separato dalla logica dei livelli. |
---

## 7. Art & Assets

---

## 8. UI

---

## 9. Tools & Data

---


## 5. Roadmap
    
- [x] 
- [ ]   
- [x] 
- [ ]   

---

## 6. Known Issues / BUGS  
- ****: 
  

---

## 7. Dependencies & Requirements


#### Requisiti:


#### Installazione:


---

## 8. Tech Stack  

- **Logic & Tools**: .
- **Database**: MySQL.
- **Infrastructure**: .
- **Collaboration**: Git/GitHub, Discord.

---

## 9. Organizzazione membri 
- **Music department**:
Vitalij , Antonio J, Antonio S
- **Programmming department**:
Leonardo, Andrea Kratos verde, Andrea , Antonio J
- **Story and dialogue**:
Antonio S, Antonio J, Vitalij
- **Art department**:
Ilaria , Andrea
- **Game designed**:
Andrea Kratos verde, Andrea
---


## 10. Licenza e Copyright  


