# Mojito Agent

Mojito agent utilizza db_core e chat_agent per costruire un ricettario di cocktail.

Inoltre si cerca di sfruttare concetti di ML e di strutturare il processo. 



---

FACCIO LA SEGUENTE GENERAZIONE CON GROUNDING E REASONING ATTIVI
Prompt:
Popola un database di ingredienti per drink.


Il tuo compito è quello di raccogliere una lista di ingredienti di diversa tipologia.

Includerai ogni ingrediente in un file di testo molto grande, prendendo diversi esempi su internet.

Capiremo così meglio diverse cose, come le marche piu diffuse, le diverse categorie di ingrediente e cosi via

---

Di seguito un esempio di contenuto per un file di testo molto ampio che raccoglie una lista di ingredienti per drink, suddivisi per tipologia. Questo file potrebbe costituire la base per un database di ingredienti, dove per ogni voce si includono anche esempi di marche diffuse e note, utili per fare riferimenti e approfondimenti:

---

**Cocktail_Ingredients_Database.txt**

---

### 1. Spiriti e Distillati

**Vodka**  
- Descrizione: Distillato di cereali o patate, molto versatile e neutro, ideale per cocktail come il Vodka Martini o il Cosmopolitan.  
- Marche Esempio:  
  - Absolut  
  - Smirnoff  
  - Grey Goose  
  - Belvedere  
  - Ketel One

**Gin**  
- Descrizione: Distillato aromatizzato con botanici (principalmente ginepro), usato in Gin Tonic, Martini e Negroni.  
- Marche Esempio:  
  - Tanqueray  
  - Bombay Sapphire  
  - Hendrick's  
  - Beefeater  
  - Plymouth

**Rum**  
- Descrizione: Distillato derivato dalla canna da zucchero, disponibile in versioni chiare, scure e speziate.  
- Marche Esempio:  
  - Bacardi (White Rum)  
  - Captain Morgan (Spiced Rum)  
  - Havana Club  
  - Malibu (cocco)

**Tequila**  
- Descrizione: Distillato prodotto dalla pianta di agave, fondamentale per Margarita e Tequila Sunrise.  
- Marche Esempio:  
  - Jose Cuervo  
  - Patron  
  - Don Julio  
  - Sauza

**Whisky/Whiskey**  
- Descrizione: Distillato ottenuto dalla fermentazione di cereali, con varianti come Scotch, Irish, Bourbon e Rye.  
- Marche Esempio:  
  - Jack Daniel's  
  - Jameson  
  - Johnnie Walker  
  - Chivas Regal  
  - Maker's Mark

**Brandy & Cognac**  
- Descrizione: Distillato ottenuto dalla fermentazione del vino, spesso invecchiato; il cognac è una tipologia pregiata di brandy.  
- Marche Esempio:  
  - Hennessy  
  - Rémy Martin  
  - Courvoisier  
  - Martell

---

### 2. Liquori e Amari

**Triple Sec e Cointreau**  
- Descrizione: Liquori all'arancia usati per dare nota agrumata; fondamentale in Margarita e Cosmopolitan.  
- Marche Esempio:  
  - Cointreau  
  - Grand Marnier (con un tocco di cognac)

**Vermouth**  
- Descrizione: Vino aromatizzato e fortificato; usato in Martini, Negroni e Manhattan.  
- Tipologie:  
  - Rosso (Martini Rosso, Carpano Antica Formula)  
  - Bianco/Secco (Martini Bianco, Noilly Prat)

**Amari e Bitter**  
- Descrizione: Liquori dal sapore amarognolo, usati per bilanciare i cocktail e aggiungere complessità.  
- Marche Esempio:  
  - Campari  
  - Aperol  
  - Fernet-Branca  
  - Amaro Montenegro  
  - Angostura Bitters  
  - Peychaud's Bitters

**Altri Liquori e Cremosi**  
- Descrizione: Liquori dal sapore dolce e cremoso, ideali per dessert e cocktail dolci.  
- Esempi:  
  - Amaretto (es. Disaronno)  
  - Kahlua  
  - Bailey's Irish Cream

---

### 3. Mixers e Succhi

**Succhi di Frutta**  
- Descrizione: Estratti di frutta freschi o concentrati, base per molti cocktail.  
- Esempi:  
  - Succo d'arancia  
  - Succo di limone  
  - Succo di lime  
  - Succo di ananas  
  - Succo di mirtillo  
  - Succo di pompelmo  
  - Succo di mela

**Bibite Gassate e Acque**  
- Descrizione: Bevande effervescenti utilizzate per allungare i cocktail.  
- Esempi:  
  - Acqua tonica  
  - Soda (acqua gassata)  
  - Cola  
  - Ginger ale  
  - Ginger beer

**Sciroppi e Dolcificanti**  
- Descrizione: Sciroppi semplici o aromatizzati per addolcire e dare corpo ai cocktail.  
- Esempi:  
  - Sciroppo di zucchero  
  - Sciroppo di menta  
  - Sciroppo di granatina (grenadine)  
  - Sciroppo di agave

---

### 4. Altri Ingredienti e Guarnizioni

**Bitter e Aromatizzanti**  
- Descrizione: Piccole quantità di bitter per aggiungere complessità; solitamente sono ingredienti concentrati.  
- Esempi:  
  - Angostura  
  - Peychaud's

**Erbe, Spezie e Aromi**  
- Descrizione: Elementi naturali per guarnire e aromatizzare i drink.  
- Esempi:  
  - Menta fresca  
  - Basilico  
  - Rosmarino  
  - Zenzero (fresco o in sciroppo)

**Frutta e Guarnizioni**  
- Descrizione: Frutta e altri elementi decorativi che completano il drink.  
- Esempi:  
  - Lime (fette o spicchi)  
  - Limone  
  - Arancia  
  - Ciliegie da cocktail  
  - Fragole  
  - Cetriolo (per gin tonic)

---

### 5. Esempi di Marche e Prodotti Specifici

**Esempi di prodotti particolari**:  
- **Vodka Premium**: Grey Goose, Belvedere  
- **Gin Artigianali**: Monkey 47, The Botanist  
- **Rum d'Altissima Qualità**: Ron Zacapa, Diplomatico  
- **Tequila 100% Agave**: Patron, Don Julio  
- **Whisky di Malto**: Glenfiddich, Lagavulin

---

### Note Aggiuntive

- **Categorie e sottocategorie**:  
  Potresti ampliare il database suddividendo ulteriormente gli ingredienti, ad esempio, distinguendo tra “Spiriti Chiari” e “Spiriti Scuri”, o tra “Succhi Freschi” e “Succhi Concentrati”.

- **Varianti regionali**:  
  Alcuni ingredienti potrebbero avere varianti regionali (es. tipi diversi di tequila, rum, o gin prodotti in diverse parti del mondo).

- **Aggiornamenti costanti**:  
  Il mondo dei cocktail è in continua evoluzione, quindi il database dovrebbe essere aggiornato periodicamente per includere nuove tendenze e marchi emergenti.

---

Questo file di testo costituisce un punto di partenza per popolare un database di ingredienti per drink. Utilizzando questo formato, è possibile importare i dati in una base MongoDB o in un altro sistema di gestione dei dati, e integrare ulteriori informazioni (come dettagli nutrizionali, descrizioni approfondite o recensioni) per ottenere un quadro completo e utile per bartender, appassionati e sviluppatori di applicazioni per cocktail.