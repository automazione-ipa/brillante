import pickle

def save_index(index, filename='index.pkl'):
    """Funzione per salvare l'indice su disco."""
    with open(filename, 'wb') as f:
        pickle.dump(index, f)


def load_index(filename='index.pkl'):
    """Funzione per caricare l'indice da disco."""
    with open(filename, 'rb') as f:
        return pickle.load(f)
