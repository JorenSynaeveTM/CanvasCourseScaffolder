from typing import List
from typing import Any
from dataclasses import dataclass
import json


@dataclass
class AssignmentGroupsItem:
    id: int
    name: str
    percentageOfTotal: int

    @staticmethod
    def from_dict(obj: Any) -> 'AssignmentGroupsItem':
        _id = int(obj.get("id"))
        _name = str(obj.get("name"))
        _percentageOfTotal = int(obj.get("percentageOfTotal"))
        return AssignmentGroupsItem(_id, _name, _percentageOfTotal)


@dataclass
class AssignmentGroups:
    assignmentGroupsItems: List[AssignmentGroupsItem]

    @staticmethod
    def from_dict(obj: Any) -> 'AssignmentGroups':
        _assignmentGroupsItems = [AssignmentGroupsItem.from_dict(y) for y in obj.get("assignmentGroupsItems")]
        return AssignmentGroups(_assignmentGroupsItems)


@dataclass
class AssignmentsItem:
    assignmentId: int
    assignmentGroupId: int
    name: str
    dueAt: str
    pointsPossible: int
    published: bool
    descriptionFile: str
    mandatory: bool

    @staticmethod
    def from_dict(obj: Any) -> 'AssignmentsItem':
        _assignmentId = int(obj.get("assignmentId"))
        _assignmentGroupId = int(obj.get("assignmentGroupId"))
        _name = str(obj.get("name"))
        _dueAt = str(obj.get("dueAt"))
        _pointsPossible = int(obj.get("pointsPossible"))
        _published = bool(obj.get("published"))
        _descriptionFile = str(obj.get("descriptionFile"))
        _mandatory = bool(obj.get("mandatory"))
        return AssignmentsItem(_assignmentId, _assignmentGroupId, _name, _dueAt, _pointsPossible, _published,
                               _descriptionFile, _mandatory)


@dataclass
class SecondAttemptItem:
    name: str
    percentageOfTotal: int
    description: str

    @staticmethod
    def from_dict(obj: Any) -> 'SecondAttemptItem':
        _name = str(obj.get("name"))
        _percentageOfTotal = int(obj.get("percentageOfTotal"))
        _description = str(obj.get("description"))
        return SecondAttemptItem(_name, _percentageOfTotal, _description)


@dataclass
class SecondAttempt:
    secondAttemptItems: List[SecondAttemptItem]

    @staticmethod
    def from_dict(obj: Any) -> 'SecondAttempt':
        _secondAttemptItems = [SecondAttemptItem.from_dict(y) for y in obj.get("secondAttemptItems")]
        return SecondAttempt(_secondAttemptItems)


@dataclass
class Assignments:
    assignmentsItems: List[AssignmentsItem]

    @staticmethod
    def from_dict(obj: Any) -> 'Assignments':
        _assignmentsItems = [AssignmentsItem.from_dict(y) for y in obj.get("assignmentsItems")]
        return Assignments(_assignmentsItems)


@dataclass
class CourseInfo:
    shortDescription: str

    @staticmethod
    def from_dict(obj: Any) -> 'CourseInfo':
        _shortDescription = str(obj.get("shortDescription"))
        return CourseInfo(_shortDescription)


@dataclass
class CourseMaterialItem:
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'CourseMaterialItem':
        _name = str(obj.get("name"))
        return CourseMaterialItem(_name)


@dataclass
class CourseMaterial:
    courseMaterialItems: List[CourseMaterialItem]

    @staticmethod
    def from_dict(obj: Any) -> 'CourseMaterial':
        _courseMaterialItems = [CourseMaterialItem.from_dict(y) for y in obj.get("courseMaterialItems")]
        return CourseMaterial(_courseMaterialItems)


@dataclass
class FirstAttemptItem:
    name: str
    percentageOfTotal: int
    description: str

    @staticmethod
    def from_dict(obj: Any) -> 'FirstAttemptItem':
        _name = str(obj.get("name"))
        _percentageOfTotal = int(obj.get("percentageOfTotal"))
        _description = str(obj.get("description"))
        return FirstAttemptItem(_name, _percentageOfTotal, _description)


@dataclass
class FirstAttempt:
    firstAttemptItems: List[FirstAttemptItem]

    @staticmethod
    def from_dict(obj: Any) -> 'FirstAttempt':
        _firstAttemptItems = [FirstAttemptItem.from_dict(y) for y in obj.get("firstAttemptItems")]
        return FirstAttempt(_firstAttemptItems)


@dataclass
class LearningGoalsItem:
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'LearningGoalsItem':
        _name = str(obj.get("name"))
        return LearningGoalsItem(_name)


@dataclass
class LearningGoals:
    learningGoalsItems: List[LearningGoalsItem]

    @staticmethod
    def from_dict(obj: Any) -> 'LearningGoals':
        _learningGoalsItems = [LearningGoalsItem.from_dict(y) for y in obj.get("learningGoalsItems")]
        return LearningGoals(_learningGoalsItems)


@dataclass
class Evaluation:
    firstAttempt: FirstAttempt
    secondAttempt: SecondAttempt

    @staticmethod
    def from_dict(obj: Any) -> 'Evaluation':
        _firstAttempt = FirstAttempt.from_dict(obj.get("firstAttempt"))
        _secondAttempt = SecondAttempt.from_dict(obj.get("secondAttempt"))
        return Evaluation(_firstAttempt, _secondAttempt)


@dataclass
class LecturersItem:
    firstname: str
    lastname: str
    email: str

    @staticmethod
    def from_dict(obj: Any) -> 'LecturersItem':
        _firstname = str(obj.get("firstname"))
        _lastname = str(obj.get("lastname"))
        _email = str(obj.get("email"))
        return LecturersItem(_firstname, _lastname, _email)


@dataclass
class Lecturers:
    LecturersItems: List[LecturersItem]

    @staticmethod
    def from_dict(obj: Any) -> 'Lecturers':
        _LecturersItems = [LecturersItem.from_dict(y) for y in obj.get("LecturersItems")]
        return Lecturers(_LecturersItems)


@dataclass
class ModuleItemsItem:
    moduleItemId: int
    moduleId: int
    type: str
    displayName: str
    published: bool
    assignmentId: int
    externalLink: str
    indent: int

    @staticmethod
    def from_dict(obj: Any) -> 'ModuleItemsItem':
        _moduleItemId = int(obj.get("moduleItemId"))
        _moduleId = int(obj.get("moduleId"))
        _type = str(obj.get("type"))
        _displayName = str(obj.get("displayName"))
        _published = bool(obj.get("published"))
        _assignmentId = int(obj.get("assignmentId"))
        _externalLink = str(obj.get("externalLink"))
        _indent = int(obj.get("indent"))
        return ModuleItemsItem(_moduleItemId, _moduleId, _type, _displayName, _published, _assignmentId, _externalLink,
                               _indent)


@dataclass
class ModuleItems:
    moduleItemsItems: List[ModuleItemsItem]

    @staticmethod
    def from_dict(obj: Any) -> 'ModuleItems':
        _moduleItemsItems = [ModuleItemsItem.from_dict(y) for y in obj.get("moduleItemsItems")]
        return ModuleItems(_moduleItemsItems)


@dataclass
class ModulesItem:
    id: int
    name: str
    published: bool

    @staticmethod
    def from_dict(obj: Any) -> 'ModulesItem':
        _id = int(obj.get("id"))
        _name = str(obj.get("name"))
        _published = bool
        return ModulesItem(_id, _name, _published)


@dataclass
class Modules:
    modulesItems: List[ModulesItem]

    @staticmethod
    def from_dict(obj: Any) -> 'Modules':
        _modulesItems = [ModulesItem.from_dict(y) for y in obj.get("modulesItems")]
        return Modules(_modulesItems)


@dataclass
class PagesItem:
    pageId: int
    name: str
    published: bool
    bodyFile: str

    @staticmethod
    def from_dict(obj: Any) -> 'PagesItem':
        _pageId = int(obj.get("pageId"))
        _name = str(obj.get("name"))
        _published = bool(obj.get("published"))
        _bodyFile = str(obj.get("bodyFile"))
        return PagesItem(_pageId, _name, _published, _bodyFile)


@dataclass
class Pages:
    pagesItems: List[PagesItem]

    @staticmethod
    def from_dict(obj: Any) -> 'Pages':
        _pagesItems = [PagesItem.from_dict(y) for y in obj.get("pagesItems")]
        return Pages(_pagesItems)


@dataclass
class PlanningItem:
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'PlanningItem':
        _name = str(obj.get("name"))
        return PlanningItem(_name)


@dataclass
class Planning:
    planningItems: List[PlanningItem]

    @staticmethod
    def from_dict(obj: Any) -> 'Planning':
        _planningItems = [PlanningItem.from_dict(y) for y in obj.get("planningItems")]
        return Planning(_planningItems)


@dataclass
class Ects:
    planning: Planning
    courseMaterial: CourseMaterial
    learningGoals: LearningGoals
    evaluation: Evaluation

    @staticmethod
    def from_dict(obj: Any) -> 'Ects':
        _planning = Planning.from_dict(obj.get("planning"))
        _courseMaterial = CourseMaterial.from_dict(obj.get("courseMaterial"))
        _learningGoals = LearningGoals.from_dict(obj.get("learningGoals"))
        _evaluation = Evaluation.from_dict(obj.get("evaluation"))
        return Ects(_planning, _courseMaterial, _learningGoals, _evaluation)


@dataclass
class CourseConfig:
    canvasCourseId: int
    canvasCourseName: str
    tileImage: str
    courseInfo: CourseInfo
    ects: Ects
    lecturers: Lecturers
    assignmentGroups: AssignmentGroups
    modules: Modules
    assignments: Assignments
    pages: Pages
    moduleItems: ModuleItems

    @staticmethod
    def from_dict(obj: Any) -> 'CourseConfig':
        _canvasCourseId = int(obj.get("canvasCourseId"))
        _canvasCourseName = str(obj.get("canvasCourseName"))
        _tileImage = str(obj.get("tileImage"))
        _courseInfo = CourseInfo.from_dict(obj.get("courseInfo"))
        _ects = Ects.from_dict(obj.get("ects"))
        _lecturers = Lecturers.from_dict(obj.get("lecturers"))
        _assignmentGroups = AssignmentGroups.from_dict(obj.get("assignmentGroups"))
        _modules = Modules.from_dict(obj.get("modules"))
        _assignments = Assignments.from_dict(obj.get("assignments"))
        _pages = Pages.from_dict(obj.get("pages"))
        _moduleItems = ModuleItems.from_dict(obj.get("moduleItems"))
        return CourseConfig(_canvasCourseId, _canvasCourseName, _tileImage, _courseInfo, _ects, _lecturers, _assignmentGroups,
                    _modules, _assignments, _pages, _moduleItems)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
