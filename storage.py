# storage.py

def read_last_value():
    try:
        with open("last_value.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def write_last_value(value):
    with open("last_value.txt", "w") as f:
        f.write(str(value))