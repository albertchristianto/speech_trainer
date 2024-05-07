import axios from "axios";
import { useMutation } from "react-query";
import { getBackendUrl } from "../../utils/baseURL";

const fetchSTT = async (data, config = {}) => {
    try {
        const response = await axios.post(getBackendUrl(`/recognize_speech?lang=${data?.lang}`), data?.data, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
            ...config
        });
        return response.data;
    } catch (error) {
        throw new Error("Failed to fetch STT");
    }
};

export const useSTT = () =>
    useMutation((data, config = {}) => fetchSTT(data, config));
