import axios, { AxiosInstance } from "axios";
import Course from "./types/Course";
import AssignmentGroup from "./types/AssignmentGroup";
import Assignment from "./types/Assignment";
import Page from "./types/Page";
import Module from "./types/Module";
import ModuleItem from "./types/ModuleItem";

const formdataHeader = {
    headers: {
        'Content-Type': `multipart/form-data;`
    }
}

class Canvas {
    axiosClient: AxiosInstance;
    baseUrl: string;
    apiKey: string;

    constructor(baseUrl: string, apiKey: string) {
        this.axiosClient = axios.create({
            baseURL: baseUrl + "/api/v1",
            headers: {
                'Authorization': `Bearer ${apiKey}`
            }
        });
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
    }

    course = {
        get: async (courseId: number): Promise<Course> => {
            const res = await this.axiosClient.get(`/courses/${courseId}`);
            return res.data as Course;
        },
        list: async () => {
            const res = await this.axiosClient.get(`/courses`);
            return res.data as Course[];
        },
        update: async (courseId: number, course: Course) => {
            const data = Course.toFormData(course);
            const res = await this.axiosClient.put(`/courses/${courseId}`, data, formdataHeader);
            return res.data;
        }
    }

    file = {
        upload: async (courseId: number, file: Blob, filename: string) => {
            let formData = new FormData();
            formData.append("file", file, filename);
            const res = await this.axiosClient.post(`/courses/${courseId}/files`, formData, formdataHeader);
            let upload_url = res.data.upload_url;
            const res2 = await this.axiosClient.post(upload_url, formData, formdataHeader);
            return res2.data.id;
        }
    }

    assignmentGroup = {
        create: async (courseId: number, assignmentGroup: AssignmentGroup) => {
            const res = await this.axiosClient.post(`/courses/${courseId}/assignment_groups`, assignmentGroup);
            return res.data;
        }
    }

    assignment = {
        create: async (courseId: number, assignment: Assignment) => {
            let formData = new FormData();
            formData.append("assignment[name]", assignment.name);
            if (assignment.assignmentGroupId) {
                formData.append("assignment[assignment_group_id]", assignment.assignmentGroupId.toString());
            }

            const res = await this.axiosClient.post(`/courses/${courseId}/assignments`, formData, formdataHeader);
            return res.data;
        }
    }

    page = {
        create: async (courseId: number, page: Page) => {
            let formdata = new FormData();
            formdata.append("wiki_page[title]", page.title);
            formdata.append("wiki_page[body]", page.body);
            formdata.append("wiki_page[published]", page.published.toString());
            const res = await this.axiosClient.post(`/courses/${courseId}/pages`, formdata, formdataHeader);
            return res.data;
        }
    }

    module = {
        create: async (courseId: number, module: Module) => {
            const data = Module.toFormData(module);
            const res = await this.axiosClient.post(`/courses/${courseId}/modules`, data, formdataHeader);
            return res.data;
        },
        update: async (courseId: number, moduleId: number, module: Module) => {
            const data = Module.toFormData(module);
            const res = await this.axiosClient.put(`/courses/${courseId}/modules/${moduleId}`, data, formdataHeader);
            return res.data;
        }
    }

    moduleItem = {
        create: async (courseId: number, moduleId: number, moduleItem: ModuleItem) => {
            const data = ModuleItem.toFormData(moduleItem);
            const res = await this.axiosClient.post(`/courses/${courseId}/modules/${moduleId}/items`, data, formdataHeader);
            return res.data;
        }
    }
}

export default Canvas;