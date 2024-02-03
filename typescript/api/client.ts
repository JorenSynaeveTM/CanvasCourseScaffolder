import axios, { AxiosResponse, AxiosRequestConfig, RawAxiosRequestHeaders } from 'axios';

export const apiClient = axios.create({
    baseURL: process.env.CANVAS_API_URL + "/api/v1",
    headers: {
        'Authorization': `Bearer ${process.env.CANVAS_API_KEY}`
    }
});