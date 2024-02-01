from typing import List, Optional
from datetime import datetime


class AssignmentGroupsItem:
    id: int
    name: str
    percentage_of_total: int

    def __init__(self, id: int, name: str, percentage_of_total: int) -> None:
        self.id = id
        self.name = name
        self.percentage_of_total = percentage_of_total


class AssignmentGroups:
    items: List[AssignmentGroupsItem]

    def __init__(self, items: List[AssignmentGroupsItem]) -> None:
        self.items = items


class AssignmentsItem:
    assignment_id: int
    assignment_group_id: int
    name: str
    due_at: datetime
    points_possible: int
    published: bool
    description_file: str
    mandatory: bool

    def __init__(self, assignment_id: int, assignment_group_id: int, name: str, due_at: datetime, points_possible: int,
                 published: bool, description_file: str, mandatory: bool) -> None:
        self.assignment_id = assignment_id
        self.assignment_group_id = assignment_group_id
        self.name = name
        self.due_at = due_at
        self.points_possible = points_possible
        self.published = published
        self.description_file = description_file
        self.mandatory = mandatory


class Assignments:
    items: List[AssignmentsItem]

    def __init__(self, items: List[AssignmentsItem]) -> None:
        self.items = items


class CourseInfo:
    short_description: str

    def __init__(self, short_description: str) -> None:
        self.short_description = short_description


class CourseMaterialItem:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name


class CourseMaterial:
    items: List[CourseMaterialItem]

    def __init__(self, items: List[CourseMaterialItem]) -> None:
        self.items = items


class FirstAttemptItem:
    name: str
    percentage_of_total: int
    description: Optional[str]

    def __init__(self, name: str, percentage_of_total: int, description: Optional[str]) -> None:
        self.name = name
        self.percentage_of_total = percentage_of_total
        self.description = description


class Attempt:
    items: List[FirstAttemptItem]

    def __init__(self, items: List[FirstAttemptItem]) -> None:
        self.items = items


class Evaluation:
    first_attempt: Attempt
    second_attempt: Attempt

    def __init__(self, first_attempt: Attempt, second_attempt: Attempt) -> None:
        self.first_attempt = first_attempt
        self.second_attempt = second_attempt


class Ects:
    planning: CourseMaterial
    course_material: CourseMaterial
    leaning_goals: CourseMaterial
    evaluation: Evaluation

    def __init__(self, planning: CourseMaterial, course_material: CourseMaterial, leaning_goals: CourseMaterial,
                 evaluation: Evaluation) -> None:
        self.planning = planning
        self.course_material = course_material
        self.leaning_goals = leaning_goals
        self.evaluation = evaluation


class LecturersItem:
    firstname: str
    lastname: str
    email: str

    def __init__(self, firstname: str, lastname: str, email: str) -> None:
        self.firstname = firstname
        self.lastname = lastname
        self.email = email


class Lecturers:
    items: List[LecturersItem]

    def __init__(self, items: List[LecturersItem]) -> None:
        self.items = items


class ModuleItemsItem:
    module_item_id: int
    module_id: int
    type: str
    display_name: str
    published: bool
    assignment_id: Optional[int]
    external_link: Optional[str]
    indent: int

    def __init__(self, module_item_id: int, module_id: int, type: str, display_name: str, published: bool,
                 assignment_id: Optional[int], external_link: Optional[str], indent: int) -> None:
        self.module_item_id = module_item_id
        self.module_id = module_id
        self.type = type
        self.display_name = display_name
        self.published = published
        self.assignment_id = assignment_id
        self.external_link = external_link
        self.indent = indent


class ModuleItems:
    items: List[ModuleItemsItem]

    def __init__(self, items: List[ModuleItemsItem]) -> None:
        self.items = items


class ModulesItem:
    id: int
    name: str
    published: bool

    def __init__(self, id: int, name: str, published: bool) -> None:
        self.id = id
        self.name = name
        self.published = published


class Modules:
    items: List[ModulesItem]

    def __init__(self, items: List[ModulesItem]) -> None:
        self.items = items


class PagesItem:
    page_id: int
    name: str
    published: bool
    body_file: str

    def __init__(self, page_id: int, name: str, published: bool, body_file: str) -> None:
        self.page_id = page_id
        self.name = name
        self.published = published
        self.body_file = body_file


class Pages:
    items: List[PagesItem]

    def __init__(self, items: List[PagesItem]) -> None:
        self.items = items


class CourseConfig:
    canvas_course_id: int
    canvas_course_name: str
    tile_image: str
    course_info: CourseInfo
    ects: Ects
    lecturers: Lecturers
    assignment_groups: AssignmentGroups
    modules: Modules
    assignments: Assignments
    pages: Pages
    module_items: ModuleItems

    def __init__(self, canvas_course_id: int, canvas_course_name: str, tile_image: str, course_info: CourseInfo,
                 ects: Ects, lecturers: Lecturers, assignment_groups: AssignmentGroups, modules: Modules,
                 assignments: Assignments, pages: Pages, module_items: ModuleItems) -> None:
        self.canvas_course_id = canvas_course_id
        self.canvas_course_name = canvas_course_name
        self.tile_image = tile_image
        self.course_info = course_info
        self.ects = ects
        self.lecturers = lecturers
        self.assignment_groups = assignment_groups
        self.modules = modules
        self.assignments = assignments
        self.pages = pages
        self.module_items = module_items
