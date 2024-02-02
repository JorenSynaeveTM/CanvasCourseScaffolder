from canvasapi import Canvas
from canvasapi.course import Course


class CanvasConnection:
    course_obj: Course

    def __init__(self, api_key: str, api_url: str, canvas_course_id: int) -> None:
        self.canvas = Canvas(api_url, api_key)
        self.course_obj = self.canvas.get_course(canvas_course_id)
