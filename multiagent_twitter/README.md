# TsunadeFi Agent - Multiagent system for openai chat and twitter posts

Per creare un agente che generi post sui temi di Curve Finance, Yearn Finance e opportunità di yield, è stato creato un
bot multi-agente che sfrutta:

- **chat_agent**: genera post di Twitter con l'**intelligenza artificiale** di OpenAI
- **twitter_agent**: posta il contenuto su Twitter tramite tweepy 

## Organizzazione del repository
Il repository è organizzato secondo la seguente struttura:

    .
    ├── agents   
    |   ├──__init__.py 
    |   └── db
    |   |   ├──__init__.py 
    |   |   └──db_core.py             # DB Core Agent
    |   └── openai
    |   |   ├──__init__.py
    |   |   ├──first_chat.py
    |   |   └──chat_agent.py          # Chat Completion Agent
    |   └── secret
    |   |   ├──__init__.py 
    |   |   └──secret.py              # Secret Agent
    |   └── twitter
    |   |   ├──__init__.py
    |   |   ├──bearer.txt
    |   |   ├──first_tweet.py 
    |   |   └──tweepy_api.py          # Twitter Post Agent
    |   └── yearn
    |       ├──__init__.py 
    |       └──yearn_ycrv_agent.py    # Yearn yCRV Agent
    ├── logic                         # Package containing the logic and the entities of the application
    |	├──__init__.py 
    |   └──entities.py                # Entities
    |
    ├── static                        # Package containing static css and js files for application
    |   └── css 
    |   |   └──styles.css             # Styles CSS File
    |   └── js
    |       └──script.js              # Script JS File
    |
    ├── templates                     # Package containing the index.html file
    |   └──index.html                 # Index Homepage HTML File
    |
    ├── tests 
    |   ├── resources                     
    |   │   ├── example-py-usage      # Example agents basic usage
    |   │   └── myswap_app.md         # Generation information about myswap satispay integration app 
    |   ├── __init__.py               
    |   ├── test_entities.py
    |   └── test_db_core.py
    |
    ├── __init__.py
    ├── README.md  
    ├── app.log   
    ├── app.py  
    └── bot.py          



## File di configurazione
Impostare un file `.env` di configurazione che risulta simile al seguente:

```bash

OPENAI_API_KEY="sk-proj-abcdef12345"

FLASK_SECRET_KEY="asdfghjkl1234567"
DB_CONNECTION_STRING="mongodb://localhost:27017/"

DB_NAME="twitter_db"

TWITTER_CLIENT_ID="aaaaaaaaaaaaa"
TWITTER_CLIENT_SECRET="bbbbbbbbbbbbbb"

TWITTER_API_KEY="key-ABCDEFGH"
TWITTER_API_SECRET="key-ABCDEFGHIJKLMNO23456"

ACCESS_TOKEN="key-ABCDEFGHIJKLMNO23456"
ACCESS_TOKEN_SECRET="key-ABCDEFGHsports"

TWITTER_BEARER_TOKEN="AAAAAAAAAAAAAAAAAAAAAkey-ABCDEFGHkey-ABCDEFGHkey-ABCDEFGHkey-ABCDEFGH"
```



## Sviluppi successivi
Il progetto in beta necessita di ulteriori fasi di raccolta dati, raccolta requisiti, analisi funzionali e tecniche, sviluppi, test unitari e di integrazione.

**Obiettivo** : realizzare un sistema di agenti in grado di creare post informativi e ben strutturati su Curve Finance, Yearn Finance e le opportunità di yield defi, garantendo contenuti di qualità e aggiornati per il pubblico di riferimento.
