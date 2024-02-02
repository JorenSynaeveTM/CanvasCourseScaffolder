from .canvas_connection import CanvasConnection
from .models.config import AssignmentGroups


class AssignmentGroupScaffolder:
    canvas_connection: CanvasConnection

    def __init__(self, canvas_connection: CanvasConnection) -> None:
        self.canvas_connection = canvas_connection

    def scaffold_assignment_groups(self, assignment_groups: AssignmentGroups) -> list[dict]:
        outcome = []
        groups = assignment_groups.assignmentGroupsItems

        # If any of the items has a weight different from 0, we need to update the course to use weighted grading
        if any(group.percentageOfTotal != 0 for group in groups):
            self.canvas_connection.course_obj.update(course={"apply_assignment_group_weights": True})

        # Create the assignment groups
        for group in groups:
            new_group = self.canvas_connection.course_obj.create_assignment_group(
                name=group.name, group_weight=group.percentageOfTotal
            )
            outcome.append({'id': group.id, 'canvas_id': new_group.id})

        return outcome
