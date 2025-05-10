$(document).ready(function () {
  let botRunning = false;
  const logOutput = $("#log-output");

  function appendLog(message) {
    logOutput.append(message + "\n");
    logOutput.scrollTop(logOutput[0].scrollHeight);
  }

  // Start bot
  $("#start-btn").click(function () {
    if (!botRunning) {
      $.ajax({
        url: "/start",
        method: "POST",
        success: function (response) {
          appendLog(response.message);
          $("#start-btn").prop("disabled", true);
          $("#stop-btn").prop("disabled", false);
          $("#fetch-trades-btn").prop("disabled", false);
          $("#fetch-order-book-btn").prop("disabled", false);
          $("#place-order-btn").prop("disabled", false); // Enable Place Order button
          botRunning = true;
          fetchLogs();
        },
        error: function (xhr) {
          appendLog("Error starting the bot: " + xhr.responseJSON.message);
        },
      });
    }
  });

  // Stop bot
  $("#stop-btn").click(function () {
    if (botRunning) {
      $.ajax({
        url: "/stop",
        method: "POST",
        success: function (response) {
          appendLog(response.message);
          $("#start-btn").prop("disabled", false);
          $("#stop-btn").prop("disabled", true);
          $("#fetch-trades-btn").prop("disabled", true);
          $("#place-order-btn").prop("disabled", true); // Disable Place Order button
          botRunning = false;
        },
        error: function (xhr) {
          appendLog("Error stopping the bot: " + xhr.responseJSON.message);
        },
      });
    }
  });

  // Place order
  $("#place-order-btn").click(function () {
    if (botRunning) {
      let tradingPair = $("#trading-pair-input").val().trim();
      let orderAmount = $("#order-amount-input").val().trim();
      let orderPrice = $("#order-price-input").val().trim();
      let orderType = $("#order-type-input").val().trim();
      let orderSide = $("#order-side-input").val().trim();


      if (!tradingPair || !orderAmount || !orderPrice || !orderType || !orderSide) {
        appendLog("Please fill in all order fields (trading pair, amount, price, type and side).");
        return;
      }

      $.ajax({
        url: "/order",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({
          trading_pair: tradingPair,
          amount: orderAmount,
          price: orderPrice,
          order_type: orderType,
          side: orderSide
        }),
        success: function (response) {
          appendLog(response.message);
        },
        error: function (xhr) {
          appendLog("Error placing order: " + xhr.responseJSON.message);
        },
      });
    } else {
      appendLog("Bot is not running. Start the bot first.");
    }
  });

  // Cancel order
  $("#cancel-order-btn").click(function () {
    if (botRunning) {
      let orderId = $("#order-id-input").val().trim(); // Get input value
  
      if (!orderId) {
        appendLog("Please enter a valid trading pair.");
        return;
      }

      $.ajax({
        url: "/cancel_order",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ order_id: orderId }), // Send JSON payload
        success: function (response) {
          appendLog(response.message);
        },
        error: function (xhr) {
          appendLog("Error for cancel order: " + xhr.responseJSON.message);
        },
      });
    } else {
      appendLog("Bot is not running. Start the bot first.");
    }
  });

  // Fetch trades manually
  $("#fetch-trades-btn").click(function () {
    if (botRunning) {
      let tradingPair = $("#trading-pair-input").val().trim(); // Get input value
  
      if (!tradingPair) {
        appendLog("Please enter a valid trading pair.");
        return;
      }

      $.ajax({
        url: "/fetch_trades",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ trading_pair: tradingPair }), // Send JSON payload
        success: function (response) {
          appendLog(response.message);
        },
        error: function (xhr) {
          appendLog("Error fetching trades: " + xhr.responseJSON.message);
        },
      });
    } else {
      appendLog("Bot is not running. Start the bot first.");
    }
  });

  // Fetch order book manually
  $("#fetch-order-book-btn").click(function () {
    if (botRunning) {
      let tradingPair = $("#trading-pair-input").val().trim();
  
      if (!tradingPair) {
        appendLog("Please enter a valid trading pair.");
        return;
      }
      $.ajax({
        url: "/fetch_order_book",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ trading_pair: tradingPair }),
        success: function (response) {
          appendLog(response.message);
        },
        error: function (xhr) {
          appendLog("Error fetching order_book: " + xhr.responseJSON.message);
        },
      });
    } else {
      appendLog("Bot is not running. Start the bot first.");
    }
  });

  // Start ping pong manually
  $("#ping-btn").click(function () {
    if (botRunning) {
      let tradingPair = $("#trading-pair-input").val().trim(); // Get input value
  
      if (!tradingPair) {
        appendLog("Please enter a valid trading pair.");
        return;
      }

      $.ajax({
        url: "/ping",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ trading_pair: tradingPair }), // Send JSON payload
        success: function (response) {
          appendLog(response.message);
        },
        error: function (xhr) {
          appendLog("Error fetching trades: " + xhr.responseJSON.message);
        },
      });
    } else {
      appendLog("Bot is not running. Start the bot first.");
    }
  });

  // Fetch account balance manually
  $("#fetch-account-balance-btn").click(function () {
    if (botRunning) {
      $.ajax({
        url: "/fetch_account_balance",
        method: "POST",
        success: function (response) {
          appendLog(response.message);
        },
        error: function (xhr) {
          appendLog("Error fetching order_book: " + xhr.responseJSON.message);
        },
      });
    } else {
      appendLog("Bot is not running. Start the bot first.");
    }
  });

  // Fetch trading pairs
  $("#fetch-trading-pairs-btn").click(function () {
    if (botRunning) {
      $.ajax({
        url: "/fetch_trading_pairs",
        method: "POST",
        success: function (response) {
          appendLog(response.message);
        },
        error: function (xhr) {
          appendLog("Error fetching order_book: " + xhr.responseJSON.message);
        },
      });
    } else {
      appendLog("Bot is not running. Start the bot first.");
    }
  });

  // Fetch logs
  function fetchLogs() {
    if (botRunning) {
      $.ajax({
        url: "/logs",
        method: "GET",
        success: function (data) {
          logOutput.text(data);
        },
        error: function () {
          appendLog("Error fetching logs.");
        },
        complete: function () {
          setTimeout(fetchLogs, 5000);
        },
      });
    }
  }
});
