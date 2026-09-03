def read_text_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def write_text_file(filename, text):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
