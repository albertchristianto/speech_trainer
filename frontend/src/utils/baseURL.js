const baseURL = 'http://127.0.0.1:8000'

export const getBackendBaseUrl = () => {
    return baseURL;
}

export const getBackendUrl = (endpoint) => {
    return baseURL + endpoint;
} 