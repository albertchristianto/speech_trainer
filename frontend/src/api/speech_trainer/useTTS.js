import axios from "axios";
import { useMutation } from "react-query";
import { getBackendUrl } from "../../utils/baseURL";

const fetchTTS = async (data, config = {}) => {
    try {
        const response = await axios.get(getBackendUrl(`/generate_sample_audio?lang=en`), { params: data }, config);
        return response.data;
    } catch (error) {
        throw new Error("Failed to fetch TTS");
    }
};

export const useTTS = () => {
    return useMutation((data, config) => fetchTTS(data, config));
}
