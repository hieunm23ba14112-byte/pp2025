import pickle, gzip, os

DATA_FILE = "students.dat"

def save(data):
    with gzip.open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)

def load():
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with gzip.open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    except:
        return None
