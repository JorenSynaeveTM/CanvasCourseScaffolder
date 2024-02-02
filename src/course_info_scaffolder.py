from .canvas_connection import CanvasConnection
from .models.config import Ects, LearningGoals


class CourseInfoScaffolder:
    canvas_connection: CanvasConnection

    def __init__(self, canvas_connection: CanvasConnection) -> None:
        self.canvas_connection = canvas_connection

    def scaffold_ects(self, ects: Ects):
        self.scaffold_learning_goals(ects.learningGoals)

    def scaffold_learning_goals(self, learning_goals: LearningGoals) -> int:
        goals = learning_goals.learningGoalsItems

        body = "<p>In dit onderdeel worden volgende leerdoelen afgetoetst:</p>"
        body += "<ol>"
        for goal in goals:
            body += f"<li>{goal.name}</li>"
        body += "</ol>"

        page_id = self.canvas_connection.course_obj.create_page(
            wiki_page={"title": "Learning goals", "body": body, "published": True}
        )

        return page_id
