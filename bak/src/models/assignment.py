class Assignment:
    def __init__(self, assignment_group, name, due_at, available_at, available_until, points, published,
                 description_content, omit_from_final_grade):
        self.id = None
        self.assignment_group = assignment_group
        self.name = name
        self.due_at = due_at
        self.available_at = available_at
        self.available_until = available_until
        self.points = points
        self.published = published
        self.description_content = description_content
        self.omit_from_final_grade = omit_from_final_grade
