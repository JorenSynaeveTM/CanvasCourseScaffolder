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
    imageId?: number

    constructor(id: number) {
        this.id = id;
    }

    static toFormData(course: Course) {
        let formdata = new FormData();
        if (course.name) formdata.append("course[name]", course.name);
        if (course.syllabusBody) formdata.append("course[syllabus_body]", course.syllabusBody);
        if (course.defaultView) formdata.append("course[default_view]", course.defaultView);
        if (course.imageId) formdata.append("course[image_id]", course.imageId.toString());
        return formdata;
    }
}

export default Course;