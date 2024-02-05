export enum CourseDefaultView {
    Feed = "feed",
    Modules = "modules",
    Syllabus = "syllabus",
    Wiki = "wiki",
    Assignments = "assignments",
}

class Course {
    id?: number;
    name?: string
    syllabusBody?: string
    defaultView?: CourseDefaultView

    constructor(id: number) {
        this.id = id;
    }

    static toFormData(course: Course) {
        let formdata = new FormData();
        if (course.name) formdata.append("course[name]", course.name);
        if (course.syllabusBody) formdata.append("course[syllabus_body]", course.syllabusBody);
        if (course.defaultView) formdata.append("course[default_view]", course.defaultView);
        return formdata;
    }
}

export default Course;