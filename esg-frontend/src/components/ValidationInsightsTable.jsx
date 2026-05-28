const ValidationInsightsTable = ({ data }) => {

    const allIssues = [

        ...(data.warnings || []),

        ...(data.suspicious || []),

        ...(data.failed || [])
    ]

    const getBadgeClass = (severity) => {

        switch (severity) {

            case "WARNING":
                return "bg-warning text-dark"

            case "SUSPICIOUS":
                return "bg-info text-dark"

            case "FAILED":
                return "bg-danger"

            default:
                return "bg-secondary"
        }
    }

    return (

        <div className="card shadow-sm p-4 mt-4">

            <div className="d-flex justify-content-between align-items-center mb-4">

                <h4>
                    Validation Insights
                </h4>

                <div className="d-flex gap-2 flex-wrap">

                    <span className="badge bg-warning text-dark">

                        Warnings:
                        {" "}
                        {data.total_warnings}

                    </span>

                    <span className="badge bg-info text-dark">

                        Suspicious:
                        {" "}
                        {data.total_suspicious}

                    </span>

                    <span className="badge bg-danger">

                        Failed:
                        {" "}
                        {data.total_failed}

                    </span>

                </div>

            </div>

            <div className="table-responsive">

                <table className="table table-bordered table-hover">

                    <thead className="table-light">

                        <tr>

                            <th>
                                Severity
                            </th>

                            <th>
                                Message
                            </th>

                            <th>
                                Record ID
                            </th>

                            <th>
                                Created At
                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        {
                            allIssues.map((issue, index) => (

                                <tr key={index}>

                                    <td>

                                        <span
                                            className={`badge ${getBadgeClass(issue.severity)}`}
                                        >

                                            {issue.severity}

                                        </span>

                                    </td>

                                    <td>
                                        {issue.message}
                                    </td>

                                    <td>
                                        {issue.record_id}
                                    </td>

                                    <td>

                                        {
                                            new Date(
                                                issue.created_at
                                            ).toLocaleString()
                                        }

                                    </td>

                                </tr>
                            ))
                        }

                    </tbody>

                </table>

            </div>

        </div>
    )
}

export default ValidationInsightsTable