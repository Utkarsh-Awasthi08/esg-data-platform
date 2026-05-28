import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend
} from 'recharts'

const MonthlyEmissionChart = ({ data }) => {

    const combined = {}

    data.fuel_emissions.forEach(item => {

        const month = item.month.substring(0, 7)
        console.log(month);
        if (!combined[month]) {

            combined[month] = {
                month,
                fuel: 0,
                electricity: 0
            }
        }

        combined[month].fuel =
            item.total_emission || 0
    })

    data.electricity_emissions.forEach(item => {

        const month = item.month.substring(0, 7)
        console.log(month);

        if (!combined[month]) {

            combined[month] = {
                month,
                fuel: 0,
                electricity: 0
            }
        }

        combined[month].electricity =
            item.total_emission || 0
    })

    const chartData = Object.values(combined)
    console.log(chartData);

    return (

        <div className="card shadow-sm p-4 h-100">

            <h4 className="mb-4">
                Monthly Emissions Trend
            </h4>

            <ResponsiveContainer
                width="100%"
                height={350}
            >

                <LineChart data={chartData}>

                    <CartesianGrid
                        strokeDasharray="3 3"
                    />

                    <XAxis dataKey="month" />

                    <YAxis />

                    <Tooltip />

                    <Legend />

                    <Line
                        type="monotone"
                        dataKey="fuel"
                        name="Fuel Emissions"
                    />

                    <Line
                        type="monotone"
                        dataKey="electricity"
                        name="Electricity Emissions"
                    />

                </LineChart>

            </ResponsiveContainer>

        </div>
    )
}

export default MonthlyEmissionChart