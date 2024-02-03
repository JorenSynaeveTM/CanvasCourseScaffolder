import axios, { AxiosInstance } from "axios";

class ApiClient {
    baseUrl: string;
    apiKey: string;
    axiosClient: AxiosInstance;

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
}

export default ApiClient;