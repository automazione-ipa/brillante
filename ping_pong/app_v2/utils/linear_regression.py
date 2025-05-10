from sklearn.linear_model import LinearRegression

def train_symbol_selector_model(data):
    """
    Train a model to select symbols based on funding rate data.
    """
    X = data[["mean", "std", "min", "max"]]
    y = data["mean"]  # Target: average funding rate (or other metric)
    model = LinearRegression()
    model.fit(X, y)
    return model

