# :smirk_cat: Gatto in fuga: I segreti dell'Obfuscation :smirk_cat:

<p align="center">
    <img width="40%" src="/img/logo_gatto_in_fuga.png">
</p>


## Sharper 2025 - Perugia

L'attività proposta è un laboratorio interattivo pensato per avvicinare il pubblico di tutte le età alla comprensione di una tecnica fondamentale della sicurezza informatica: l'obfuscation. Questo concetto viene esplorato attraverso un gioco in cui i partecipanti dovranno guidare un gatto attraverso diversi livelli, cercando di evitare il guardiano. Ogni livello presenterà una difficoltà crescente, richiedendo strategie sempre più sofisticate per non farsi "catturare".

Il legame con l'informatica risiede nel fatto che il malware, per sfuggire agli antivirus, adotta tecniche simili a quelle utilizzate dal gatto nel gioco: cerca di agire in modo poco evidente, modificando il proprio comportamento per non essere riconosciuto. L'obfuscation è infatti una tecnica che consente di rendere illeggibile il codice malevolo senza alterarne la funzionalità, proprio come il gatto cerca di "confondere" il guardiano per mettersi in salvo.
Attraverso questo approccio ludico-didattico, ci proponiamo di spiegare concetti complessi in modo intuitivo e coinvolgente, soprattutto per i più giovani. Il gioco sarà accessibile e divertente, ma allo stesso tempo offrirà spunti di riflessione su temi attuali come la cybersecurity e la consapevolezza digitale.

A cura di: **Dipartimento di Matematica e Informatica** (Jacopo Di Benedetto, Stefano Bistarelli, Cristian Cerami, Marco Cuccarini, Sara Geoli, Chiara Luchini, Ivan Mercanti, Francesco Santini, Carlo Taticchi, Luca Maria Tutino).

Al seguente link i [dettagli dell'evento](https://www.sharper-night.it/evento/gatto-in-fuga-i-segreti-dellobfuscation/).

## Installazione gioco

Prerequisiti:
- Aver installato Python 3
- Avere a disposizione e aggiornato il gestore di pacchetti `pip`

Fai il download del gioco:
```
git clone https://github.com/Meht-evaS/Sharper-2025.git
```

Installa la libreria `Pygame`:
```
pip install pygame
```

Se per muoverti nel gioco vuoi usare il Joystick PS3 (su Windows), guarda la seguente [guida di installazione dei driver](https://docs.nefarius.at/projects/DsHidMini/) (**DsHidMini**).


## Obiettivo e funzionamento gioco

<p align="center">
    <img width="100%" src="/img/schermata_intro.png">
</p>

### Obiettivo

<p align="center">
    <img width="100%" src="/img/schermata_campo_gioco.png">
</p>

Garfield, il celebre gatto goloso e astuto, si è improvvisato hacker per una giornata speciale: la sua missione è attraversare il campo da gioco per raggiungere il computer in fondo al livello e installare... un malware!  
Ma ad ostacolarlo c'è Avast, l'accalappiagatti digitale, pronto a bloccare ogni tentativo sospetto.

Il campo da gioco è pieno di insidie: ad ogni livello, Avast è programmato per intercettare **specifiche sequenze di movimenti**. Se Garfield esegue una sequenza di passi che Avast sa riconoscere, scatta la cattura e il tentativo fallisce!

Questi pattern cambiano di livello in livello: spetta a te scoprire, sperimentando, quali movimenti sono "sicuri" e quali invece fanno scattare l'allarme.

Riuscirai a trovare la strada giusta, aggirando le sequenze sospette e ingannando la sorveglianza di Avast?  

### Funzionamento

<p align="center">
    <img width="100%" src="/img/schermata_esempio.png">
</p>

**Prima di iniziare a giocare**, ti consigliamo di cliccare sul menù "**Esempio funzionamento**".  
Qui potrai vedere chiaramente la sequenza di movimenti che Avast (l'accalappiagatti) sa riconoscere e capire come funziona la meccanica del gioco. In questo livello d'esempio puoi muoverti liberamente con le **frecce della tastiera** o del **joystick**, ma appena esegui la sequenza di passi sospetta, vieni subito catturato!

Sulla **destra dello schermo** trovi la lista dei movimenti che hai eseguito: questa lista ti aiuta a capire quali azioni ti hanno portato alla cattura.  

Nel livello d'esempio, i movimenti che hanno causato la cattura vengono **colorati di rosso**, così puoi vedere immediatamente dove hai sbagliato.

#### **Livelli di difficoltà**

Il gioco offre **tre livelli di difficoltà**:

- **Facile**:  
  - Vedi sempre la lista dei movimenti eseguiti.
  - I passi che hanno portato alla cattura vengono evidenziati in rosso.
  - Puoi facilmente individuare i pattern sospetti.

- **Normale**:  
  - Vedi la lista dei movimenti, ma **non c'è più alcun suggerimento** sui pattern che ti hanno fatto catturare.
  - Devi ragionare e sperimentare per capire quali sequenze sono pericolose.

- **Difficile**:  
  - **Non vedi più la lista dei movimenti**.
  - Devi ricordare i tuoi passi e affidarti solo alla tua memoria e intuizione!

#### **Suggerimento per superare i livelli**

- Per completare tutti i livelli, **ogni volta che vieni catturato guarda attentamente TUTTI i suggerimenti che compaiono sullo schermo**.
- PS. Il livello 3 non è impossibile! :eyes:

---

**In sintesi:**  
Muoviti con le frecce (o il joystick), evita di eseguire le sequenze che Avast riconosce, osserva la lista dei movimenti e i suggerimenti, e diventa il Garfield più astuto di sempre!

