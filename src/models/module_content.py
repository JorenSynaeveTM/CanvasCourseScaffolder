from enum import Enum


class ModuleContentType(Enum):
    ASSIGNMENT = 1
    URL = 2
    QUIZ = 3
    FILE = 4
    SUB_HEADER = 5


class ModuleContent:
    def __init__(self, type, display_name, published, assignment, url, quiz, file_path, indent=0):
        self.type = type
        self.display_name = display_name
        self.published = published
        self.assignment = assignment
        self.url = url
        self.quiz = quiz
        self.file_path = file_path
        self.indent = indent
