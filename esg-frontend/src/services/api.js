import axios from "axios";

const api = axios.create({
    baseURL: "https://esg-data-platform-km4q.onrender.com/api"
});

export default api;