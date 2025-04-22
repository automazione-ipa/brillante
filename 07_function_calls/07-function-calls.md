Di seguito troverai una panoramica completa della feature **Function Calling** di OpenAI, con spiegazione dello schema JSON da completare, caratteristiche principali, un esempio pratico in Python e i riferimenti a progetti GitHub e guide utili per sfruttare al meglio questa funzionalità.

In sintesi, la **Function Calling** permette di definire un elenco di “funzioni” (o strumenti) tramite uno **schema JSON**, in modo che il modello riconosca quando e quali chiamate effettuare, restituendo output validi e strutturati. Il parametro `functions` di una chiamata al modello è un array di oggetti, ciascuno con i campi `name`, `description` e `parameters` (che a loro volta è un oggetto conforme a JSON Schema). Il modello valuta automaticamente se invocare una funzione in base al contesto del prompt, e restituisce nel messaggio di risposta un JSON con `name` e `arguments` da eseguire nel codice dell’applicazione. Questa integrazione abilita assistenti AI “tool-aware”, facilita l’enforcement di output validi e apre a integrazioni profonde con API esterne. 

## 1. Panoramica della Function Calling  
### 1.1 Cos’è e perché usarla  
La Function Calling fornisce un modo potente e flessibile per interfacciare i modelli OpenAI con il tuo codice o servizi esterni, consentendo di trasformare output testuali in chiamate di funzioni programmatiche citeturn0search0.  
Puoi descrivere funzioni all’Assistant API e il modello restituirà in modo intelligente il nome della funzione e gli argomenti da chiamare, anziché un testo libero citeturn0search2.  
Quando includi nel request uno o più strumenti (funzioni), il modello decide automaticamente se e quale funzione invocare in base al contesto fornito citeturn0search16.  
Inoltre, grazie all’integrazione con **Structured Outputs**, è possibile garantire che l’assistant restituisca sempre risposte aderenti a un JSON Schema definito, migliorando l’affidabilità degli output citeturn0search3.  

### 1.2 Ambiti d’impiego  
Con Function Calling puoi:  
- **Collegare LLM a tool esterni** (es. API meteo, database, servizi di pagamento) citeturn0search9.  
- **Creare assistenti AI autonomi**, in grado di eseguire operazioni specifiche (controllo orario, prenotazioni) citeturn0search10.  
- **Enforce di output strutturati** per pipeline di dati, reportistica o analisi automatizzate citeturn0search3.  

## 2. Schema JSON delle funzioni  
### 2.1 Struttura generale  
Lo schema JSON per il parametro `functions` ha la forma seguente:

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "description": "Identificatore univoco della funzione"
      },
      "description": {
        "type": "string",
        "description": "Breve spiegazione dello scopo della funzione"
      },
      "parameters": {
        "type": "object",
        "properties": {
          // Definizione dei singoli parametri della funzione
        },
        "required": [
          // Elenco dei parametri obbligatori
        ],
        "additionalProperties": false
      }
    },
    "required": ["name", "description", "parameters"]
  }
}
```
- **type: array** → il valore di `functions` è una lista di definizioni di funzione citeturn0search19.  
- **items.type: object** → ogni elemento descrive una funzione con campi strutturati.  
- **required** → obbliga la presenza di `name`, `description` e `parameters` per ciascuna funzione.  

### 2.2 I campi chiave  
- **name** (`string`): unique identifier; deve essere un nome privo di spazi e simboli particolari citeturn0search19.  
- **description** (`string`): breve testo per aiutare il modello a capire quando usare la funzione citeturn0search19.  
- **parameters** (`object`): JSON Schema Draft-07 che descrive i parametri di input:
  - `properties`: mappa di nome→schema del parametro (tipo, descrizione, enum, pattern, ecc.) citeturn0search19.  
  - `required`: array dei nomi obbligatori.  
  - `additionalProperties: false`: per limitare input indesiderati.  

### 2.3 Tipologie di parametri supportati  
Gli schemi possono includere:  
- **tipi primitivi**: `string`, `number`, `integer`, `boolean` citeturn0search11.  
- **array**: con `items` che definisce il tipo degli elementi.  
- **object annidati**: per strutture più complesse (es. filtri multipli).  
- **enum**, `minimum`/`maximum`, `pattern`, ecc. come in JSON Schema standard citeturn0search11.  

## 3. Flusso di integrazione  
1. **Definizione delle funzioni** in forma di array JSON conforme allo schema.  
2. **Chiamata a ChatCompletion.create** includendo `functions=[…]` e `function_call="auto"` (o il nome specifico).  
3. **Ricezione** del messaggio con `role="assistant"`, `content=null` e `function_call` contenente `name` e `arguments` citeturn0search5.  
4. **Esecuzione** della funzione nel tuo codice, passando gli `arguments` deserializzati.  
5. **Invio del risultato** come messaggio con `role="function"` per proseguire la conversazione.  

## 4. Esempio pratico in Python  
```python
import openai, json

functions = [
  {
    "name": "get_current_weather",
    "description": "Ottiene le condizioni meteo attuali in una località",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "Città e stato, es. Florence, Italy"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"]
        }
      },
      "required": ["location"]
    }
  }
]

response = openai.ChatCompletion.create(
  model="gpt-4o",
  messages=[{"role":"user","content":"Che tempo fa a Firenze?"}],
  functions=functions,
  function_call="auto"
)

if (call := response.choices[0].message.function_call):
    name = call.name
    args = json.loads(call.arguments)
    # Es. name == "get_current_weather", args["location"] == "Firenze, Italy"
    weather = get_current_weather_api(**args)  # implementa tu la chiamata esterna
    # Invia il risultato al modello
    followup = openai.ChatCompletion.create(
      model="gpt-4o",
      messages=[
        {"role":"assistant","content":None,"function_call":call},
        {"role":"function","name":name,"content":json.dumps(weather)}
      ]
    )
    print(followup.choices[0].message.content)
```

## 5. Progetti GitHub di riferimento  
- **Simoon-F/openai-function-calling-use-examples**: esempi base in Python e Streamlit citeturn0search1.  
- **jakecyr/openai-function-calling**: helper per generare dizionari JSON Schema in Python citeturn0search8.  
- **openai/openai-cookbook**: notebook “How to call functions with chat models” citeturn0search5.  
- **john-carroll-sw/chat-completions-function-calling-examples**: collezione di script focalizzati su function calling citeturn0search18.  
- **dkhundley/openai-api-tutorial**: notebook Jupyter con esempi di function calling citeturn0search13.  

## 6. Guide e risorse consigliate  
- **Documentazione ufficiale Function Calling** (OpenAI Platform) citeturn0search0turn0search2  
- **Function Calling Developer Guide** (Help Center) citeturn0search9  
- **Azure OpenAI Function Calling** (Microsoft Learn) citeturn0search10  
- **Medium: A clear guide to OpenAI function calling with Python** citeturn0search7  
- **Tutorial DataCamp** “OpenAI Function Calling” citeturn0search4  
- **Vellum AI Blog** “OpenAI Function Calling Tutorial for Developers” citeturn0search14  
- **Cobus Greyling su Medium** “Practical Examples of OpenAI Function Calling” citeturn0search17  

Con queste informazioni hai tutto il necessario per definire correttamente lo schema JSON, integrare function call nelle tue applicazioni e approfondire tramite esempi e guide di alta qualità. Buono sviluppo!
