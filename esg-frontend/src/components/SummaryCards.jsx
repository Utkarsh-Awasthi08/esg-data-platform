const SummaryCards = ({ data }) => {

    const cards = [
        {
            title: 'Total Emission',
            value: data.total_emission
        },
        {
            title: 'Fuel Emission',
            value: data.fuel_emission
        },
        {
            title: 'Electricity Emission',
            value: data.electricity_emission
        },
        {
            title: 'Procurement Emission',
            value: data.procurement_emission
        }
    ]

    return (
        <div className='summary-grid'>

            {
                cards.map((card, index) => (

                    <div className='summary-card' key={index}>

                        <h3>{card.title}</h3>

                        <h2>{card.value}</h2>

                    </div>
                ))
            }
        </div>
    )
}

export default SummaryCards;