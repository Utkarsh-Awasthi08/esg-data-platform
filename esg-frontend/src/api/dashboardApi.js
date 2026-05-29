import axios from 'axios'

const BASE_URL = 'https://esg-data-platform-km4q.onrender.com/api'

export const getDashboardData = async () => {

    const response = await axios.get(
        `${BASE_URL}/dashboard/`
    )

    return response.data
}