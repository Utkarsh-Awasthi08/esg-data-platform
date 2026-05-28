import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    CartesianGrid
} from 'recharts'

const ScopeBarChart = ({ data }) => {

    const chartData = [
        {
            scope: 'Scope 1',
            value: data.scope_1
        },
        {
            scope: 'Scope 2',
            value: data.scope_2
        },
        {
            scope: 'Scope 3',
            value: data.scope_3
        }
    ]

    return (
        <div className='chart-card'>

            <h2>Scope Breakdown</h2>

            <ResponsiveContainer width='100%' height={350}>

                <BarChart data={chartData}>

                    <CartesianGrid strokeDasharray='3 3' />

                    <XAxis dataKey='scope' />

                    <YAxis />

                    <Tooltip />

                    <Bar dataKey='value' fill='#8884d8' />

                </BarChart>

            </ResponsiveContainer>

        </div>
    )
}

export default ScopeBarChart