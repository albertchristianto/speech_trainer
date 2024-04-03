import axios from "axios";
import { useMutation } from "react-query";
import { getBackendUrl } from "../../utils/baseURL";

const fetchGetScore = async (data, config = {}) => {
    try {
        const response = await axios.get(getBackendUrl(`/get_score?lang=${data?.lang}`), { params: data?.data }, config);
        return response.data;
    } catch (error) {
        throw new Error("Failed to fetch Get Score");
    }
};

export const useGetScore = () =>
    useMutation((data, config = {}) => fetchGetScore(data, config));