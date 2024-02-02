from src.course_info_scaffolder import CourseInfoScaffolder
from src.models.config import CourseConfig
from src.canvas_connection import CanvasConnection
from src.assignment_group_scaffolder import AssignmentGroupScaffolder
import json
import os

CANVAS_API_KEY = os.environ.get("CANVAS_API_KEY")
CANVAS_API_URL = os.environ.get("CANVAS_API_URL")


def get_config():
    with open('config.json', 'r') as file:
        my_json_string = file.read()
    json_string = json.loads(my_json_string)
    course_config = CourseConfig.from_dict(json_string)
    return course_config


if __name__ == "__main__":
    config = get_config()
    canvas_connection = CanvasConnection(CANVAS_API_KEY, CANVAS_API_URL, config.canvasCourseId)
    course_info_scaffolder = CourseInfoScaffolder(canvas_connection)
    course_info_scaffolder.scaffold_ects(config.ects)
    assignment_group_scaffolder = AssignmentGroupScaffolder(canvas_connection)
    assignment_group_outcome = assignment_group_scaffolder.scaffold_assignment_groups(config.assignmentGroups)
    print(assignment_group_outcome)
