export interface CourseConfig {
  canvasCourseId: number
  canvasCourseName: string
  tileImage: string
  courseInfo: CourseInfo
  ects: Ects
  lecturers: Lecturers
  assignmentGroups: AssignmentGroups
  modules: Modules
  assignments: Assignments
  pages: Pages
  moduleItems: ModuleItems
}

export interface CourseInfo {
  shortDescription: string
}

export interface Ects {
  planning: Planning
  courseMaterial: CourseMaterial
  learningGoals: LearningGoals
  evaluation: Evaluation
}

export interface Planning {
  planningItems: PlanningItem[]
}

export interface PlanningItem {
  name: string
}

export interface CourseMaterial {
  courseMaterialItems: CourseMaterialItem[]
}

export interface CourseMaterialItem {
  name: string
}

export interface LearningGoals {
  learningGoalsItems: LearningGoalsItem[]
}

export interface LearningGoalsItem {
  name: string
}

export interface Evaluation {
  firstAttempt: FirstAttempt
  secondAttempt: SecondAttempt
}

export interface FirstAttempt {
  firstAttemptItems: FirstAttemptItem[]
}

export interface FirstAttemptItem {
  name: string
  percentageOfTotal: number
  description: string
}

export interface SecondAttempt {
  secondAttemptItems: SecondAttemptItem[]
}

export interface SecondAttemptItem {
  name: string
  percentageOfTotal: number
  description: string
}

export interface Lecturers {
  LecturersItems: LecturersItem[]
}

export interface LecturersItem {
  firstname: string
  lastname: string
  email: string
}

export interface AssignmentGroups {
  assignmentGroupsItems: AssignmentGroupsItem[]
}

export interface AssignmentGroupsItem {
  id: number
  name: string
  percentageOfTotal: number
}

export interface Modules {
  modulesItems: ModulesItem[]
}

export interface ModulesItem {
  id: number
  name: string
  published: boolean
  position: number
}

export interface Assignments {
  assignmentsItems: AssignmentsItem[]
}

export interface AssignmentsItem {
  assignmentId: number
  assignmentGroupId: number
  name: string
  dueAt: string
  pointsPossible: number
  published: boolean
  descriptionFile: string
  mandatory: boolean
}

export interface Pages {
  pagesItems: PagesItem[]
}

export interface PagesItem {
  pageId: number
  name: string
  published: boolean
  bodyFile: string
}

export interface ModuleItems {
  moduleItemsItems: ModuleItemsItem[]
}

export interface ModuleItemsItem {
  moduleItemId: number
  moduleId: number
  type: string
  title: string
  published: boolean
  assignmentId: number
  exteralUrl: string
  indent: number
}
