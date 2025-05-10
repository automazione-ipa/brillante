# Trade Bot Controller

A Flask-based trading bot that integrates with the Tothemoon API to perform various trading operations. This application provides a web interface for bot control, order placement, and real-time logging of bot activities.
Below are the only updated sections to include in your README:

---

### Requirements

Create a `requirements.txt` file with the following content (adjust versions as needed):

```txt
flask==2.0.1
requests==2.26.0
```

---

### Quick Start Guide

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Zakarin1998/ping_pong
   cd ping_pong
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python -m run.py
   ```

## Overview

The Trade Bot Controller allows you to:
- Start and stop the trading bot.
- Fetch the latest trades, order book, trading pairs, and account balances.
- Execute a "ping-pong" trading strategy between two accounts.
- View real-time logs via a user-friendly frontend interface.

The bot logic is encapsulated in a Flask blueprint (in `bot.py`), and the frontend is built using HTML, CSS, and jQuery.

## Features

- **Bot Control:**  
  Start and stop the bot with dedicated API endpoints.
  
- **Trading Operations:**  
  - Fetch latest trades for a given trading pair.
  - Retrieve order book details.
  - List available trading pairs.
  - Fetch account balances.
  - Execute a ping-pong strategy that alternates buy and sell orders between two accounts.
  
- **Order Management:**  
  The bot places orders using the Tothemoon API and logs key details like order IDs and prices.

- **Real-Time Logging:**  
  All actions, including errors and status updates, are logged with timestamps and can be viewed via the web interface.

- **Error Handling:**  
  Robust error handling is implemented with try/except blocks and descriptive log messages for easier debugging.

## Architecture

### Backend

- **Flask & Blueprints:**  
  The bot logic is defined in `bot.py` using a Flask blueprint (`bot_blueprint`), making it modular and easy to integrate into larger Flask applications.
  
- **API Integration:**  
  Uses a custom `MoonApi` client (from `app.moon_api`) to interact with the Tothemoon API. Two different accounts are supported via separate credentials.

- **Utility Functions:**  
  Helper functions (from `app.utils`) such as `pair`, `price_rnd`, `random_range`, `random_int`, and `simple_mid_price` are used for trade calculations and logging.

### Frontend

- **HTML & CSS:**  
  A responsive web interface that allows users to control the bot, submit trading parameters, and view logs.
  
- **JavaScript (jQuery):**  
  Manages AJAX calls to backend endpoints for operations like starting/stopping the bot, fetching trades, order book, account balances, and triggering the ping-pong strategy. Also handles dynamic log updates.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/trade-bot-controller.git
   cd trade-bot-controller
   ```

2. **Create a Virtual Environment and Install Dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure API Keys:**
   Update the API credentials in `bot.py`:
   ```python
   TOTHMOON_API_BASE_URL = "https://api.tothemoon.com"
   ACCESS_KEY = "0l5n2Kl+QsWmaA8zl6rBoA=="
   SECRET_KEY = "ZZmbQKwop94MRvKgB5MxXkrXCv69iYtluyolwPndp40="
   
   # Credentials for account 2
   API_KEY_2 = "your_api_key_account_2"
   API_SECRET_2 = "your_api_secret_account_2"
   ```
   For production, consider using environment variables or a secure configuration manager.

## Usage

### Running the Application

1. **Set the Flask App and Run the Server:**
   ```bash
   export FLASK_APP=app.py
   flask run
   ```
   Or use a custom run script:
   ```bash
   python run.py
   ```

2. **Access the Web Interface:**
   Open your browser and navigate to `http://localhost:5000` to see the Trade Bot Controller.

### Bot Control & Operations

- **Start/Stop Bot:**  
  Use the "Start Bot" and "Stop Bot" buttons to control the bot. When started, the bot logs activity and periodically performs operations based on user inputs.

- **Fetch Data:**  
  Use dedicated buttons to:
  - Fetch the latest trades (`/fetch_trades`)
  - Retrieve the order book (`/fetch_order_book`)
  - Get account balances (`/fetch_account_balance`)
  - List trading pairs (`/fetch_trading_pairs`)
  - Trigger the ping-pong trading strategy (`/ping`)

- **Logging:**  
  The bot logs every operation (trade orders, errors, etc.) with timestamps. Logs update automatically in the "Bot Logs" section.

## API Endpoints

The following endpoints are provided by the bot's Flask blueprint:

- **POST `/start`**  
  Start the bot. Returns a message indicating the bot has started.

- **POST `/stop`**  
  Stop the bot. Returns a message indicating the bot has stopped.

- **POST `/fetch_trades`**  
  Fetch and log the latest trades for the specified trading pair.  
  **Payload Example:**
  ```json
  { "trading_pair": "BTC_USD" }
  ```

- **POST `/fetch_order_book`**  
  Retrieve and log the current order book for the specified trading pair.

- **POST `/fetch_trading_pairs`**  
  Fetch and log all available trading pairs.

- **POST `/fetch_account_balance`**  
  Fetch and log the account balances.

- **POST `/ping`**  
  Trigger the ping-pong trading strategy on the specified trading pair.

- **GET `/logs`**  
  Retrieve the latest 50 log messages.

## Code Overview

### `bot.py`

- **API Client Initialization:**  
  Two instances of `MoonApi` are created—one for the primary account and one for a secondary account—to enable the ping-pong strategy.

- **Trading Functions:**  
  Functions such as `fetch_trades`, `fetch_trading_pairs`, `fetch_account_balance`, `fetch_order_book`, and `ping_pong_bot` handle the various trading operations and log their outputs.

- **Utility Functions:**  
  - `append_log(message)`: Adds a timestamped message to the log.
  - `random_wait(random_time)`: Waits for a random time interval before continuing the cycle.
  - `get_mid_price(trading_pair)`: Calculates the mid-price from the current order book.

- **Flask Endpoints:**  
  The blueprint exposes endpoints for starting/stopping the bot, fetching data, and triggering operations. Each endpoint ensures the bot is running before executing actions and logs both successful and error states.

### Frontend Files

- **HTML & CSS:**  
  The frontend includes a main page (`index.html`) with controls for bot actions and a log display area.
  
- **JavaScript (`app.js`):**  
  Uses jQuery to:
  - Send AJAX requests to the Flask endpoints.
  - Update the UI based on responses.
  - Auto-refresh logs every 5 seconds while the bot is running.

## Error Handling & Logging

- **Error Handling:**  
  Each backend operation uses try/except blocks to catch exceptions and log errors.  
- **Logging:**  
  All key events (bot start/stop, API call successes/failures, order details) are logged with timestamps and are visible on the frontend.
- **Real-time Updates:**  
  The frontend continuously polls the `/logs` endpoint to ensure you always see the latest activity.

## Contributing

Contributions are welcome! Please fork this repository, make your improvements, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions or support, please contact [your.email@example.com](mailto:alessandrobrillante78@gmail.com).
