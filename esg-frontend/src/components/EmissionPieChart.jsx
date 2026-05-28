import {
    PieChart,
    Pie,
    Tooltip,
    Cell,
    Legend,
    ResponsiveContainer
} from 'recharts'

const EmissionPieChart = ({ data }) => {

    const chartData = [
        {
            name: 'Fuel',
            value: data.fuel_emission
        },
        {
            name: 'Electricity',
            value: data.electricity_emission
        },
        {
            name: 'Procurement',
            value: data.procurement_emission
        }
    ]

    const COLORS = [
        '#0088FE',
        '#00C49F',
        '#FFBB28'
    ]

    return (
        <div className='chart-card'>

            <h2>Emission Sources</h2>

            <ResponsiveContainer width='100%' height={350}>

                <PieChart>

                    <Pie
                        data={chartData}
                        dataKey='value'
                        outerRadius={120}
                        label
                    >
                        {
                            chartData.map((entry, index) => (
                                <Cell
                                    key={index}
                                    fill={COLORS[index % COLORS.length]}
                                />
                            ))
                        }
                    </Pie>

                    <Tooltip />

                    <Legend />

                </PieChart>

            </ResponsiveContainer>

        </div>
    )
}

export default EmissionPieChart