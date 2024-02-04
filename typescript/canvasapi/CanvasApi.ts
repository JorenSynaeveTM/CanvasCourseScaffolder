import axios, { AxiosInstance } from "axios";
import Course from "./types/Course";
import AssignmentGroup from "./types/AssignmentGroup";
import Assignment from "./types/Assignment";

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

            // Log all formdata keys and values
            for (var key of formData.keys()) {
                console.log(key);
            }
            for (var value of formData.values()) {
                console.log(value);
            }

            const res = await this.axiosClient.post(`/courses/${courseId}/assignments`, formData, {
                headers: {
                    'Content-Type': `multipart/form-data;`
                }
            });
            return res.data;
        }
    }
}

export default Canvas;