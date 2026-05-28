import { useEffect, useState } from 'react'

import { getDashboardData } from '../api/dashboardApi'

import api from '../services/api'

import SummaryCards from '../components/SummaryCards'
import EmissionPieChart from '../components/EmissionPieChart'
import ScopeBarChart from '../components/ScopeBarChart'
import ValidationIssueChart from '../components/ValidationIssueChart'

import MonthlyEmissionChart from '../components/MonthlyEmissionChart'

import ValidationInsightsTable from '../components/ValidationInsightsTable'

const Dashboard = () => {

    const [dashboardData, setDashboardData] = useState(null)

    const [monthlyData, setMonthlyData] = useState(null)

    const [validationData, setValidationData] = useState(null)

    useEffect(() => {

        fetchDashboardData()

        fetchMonthlyData()

        fetchValidationInsights()

    }, [])

    const fetchDashboardData = async () => {

        try {

            const data = await getDashboardData()

            setDashboardData(data)

        } catch (error) {

            console.error(error)
        }
    }

    const fetchMonthlyData = async () => {

        try {

            const response = await api.get(
                '/analytics/monthly-emissions/'
            )

            setMonthlyData(response.data)

        } catch (error) {

            console.error(error)
        }
    }

    const fetchValidationInsights = async () => {

        try {

            const response = await api.get(
                '/analytics/validation-insights/'
            )

            setValidationData(response.data)

        } catch (error) {

            console.error(error)
        }
    }

    if (
        !dashboardData ||
        !monthlyData ||
        !validationData
    ) {

        return <h2>Loading Dashboard...</h2>
    }

    return (

        <div className='container mt-4'>

            <h1 className='mb-4'>
                ESG Analytics Dashboard
            </h1>

            <SummaryCards data={dashboardData} />

            <div className='row'>

                <div className='col-md-6 mb-4'>

                    <EmissionPieChart
                        data={dashboardData}
                    />

                </div>

                <div className='col-md-6 mb-4'>

                    <ScopeBarChart
                        data={dashboardData}
                    />

                </div>

                <div className='col-md-6 mb-4'>

                    <ValidationIssueChart
                        data={dashboardData}
                    />

                </div>

                <div className='col-md-6 mb-4'>

                    <MonthlyEmissionChart
                        data={monthlyData}
                    />

                </div>

            </div>

            <ValidationInsightsTable
                data={validationData}
            />

        </div>
    )
}

export default Dashboard