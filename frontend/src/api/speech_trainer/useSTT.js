import axios from "axios";
import { useMutation } from "react-query";
import { getBackendUrl } from "../../utils/baseURL";

const fetchSTT = (data) => {
    try {
        const response = axios.post(getBackendUrl(`/recognize_speech?lang=en`), data, {
            headers: {
                'Content-Type': 'multipart/form-data',
            }
        });
        return response.data;
    } catch (error) {
        throw new Error("Failed to fetch STT");
    }
};

export const useSTT = () =>
    useMutation(data => fetchSTT(data));
