import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer
} from 'recharts'

const ValidationIssueChart = ({ data }) => {

    const chartData = [
        {
            severity: 'FAILED',
            value: data.failed_issues
        },
        {
            severity: 'WARNING',
            value: data.warning_issues
        },
        {
            severity: 'SUSPICIOUS',
            value: data.suspicious_issues
        }
    ]

    return (
        <div className='chart-card'>

            <h2>Validation Issues</h2>

            <ResponsiveContainer width='100%' height={350}>

                <BarChart data={chartData}>

                    <XAxis dataKey='severity' />

                    <YAxis />

                    <Tooltip />

                    <Bar dataKey='value' fill='#82ca9d' />

                </BarChart>

            </ResponsiveContainer>

        </div>
    )
}

export default ValidationIssueChart