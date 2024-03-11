import axios from "axios";
import { useMutation } from "react-query";
import { getBackendUrl } from "../../utils/baseURL";

const fetchTTS = (data) => {
    try {
        const response = axios.get(getBackendUrl(`/generate_sample_audio?lang=en`), { params: data });
        return response.data;
    } catch (error) {
        throw new Error("Failed to fetch TTS");
    }
};

export const useTTS = () =>
    useMutation(data => fetchTTS(data));
