import { AxiosInstance } from 'axios';
import { apiClient, createClient } from './client';

class Canvas {
    client: AxiosInstance;
    baseUrl: string;
    token: string;

    constructor(baseUrl: string, token: string) {
        this.baseUrl = baseUrl;
        this.token = token;
        this.client = createClient(baseUrl + "/api/v1", token);
    }

    course = {
        path: "/courses",

        get: async (id: number) => {
            return this.client.get(`${this.course.path}/${id}`);
        }
    }
}

export default Canvas;