import re

replacement_patterns = [
    (
        r"Agricultural and Biological Engineering",
        "Agricultural and Biosystems Engineering",
    ),
    (r"Industrial Engineering", "Industrial and Manufacturing Systems Engineering"),
    (r"Materials Science & Engineering", "Materials Science and Engineering"),
    (
        r"Molecular, Cellular, and Developmental Biology",
        "Molecular, Cellular and Developmental Biology",
    ),
    (r"Education Leadership", "Education"),
    (r"Agriculture Engineering", "Agricultural and Biosystems Engineering"),
    (r"Agricultural Engineering", "Agricultural and Biosystems Engineering"),
    (r"Materials Science", "Materials Science and Engineering"),
    (r"Electrical and Computer Engineering", "Computer Engineering"),
    (r"Nutritional Science", "Nutritional Sciences"),
]


class RegexpReplacer(object):
    def __init__(self, patterns=replacement_patterns):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]

    def replace(self, text):
        s = text
        for (pattern, repl) in self.patterns:
            s = re.sub(pattern, repl, s)
        return s
