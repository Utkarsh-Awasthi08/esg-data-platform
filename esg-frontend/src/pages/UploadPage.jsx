import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function UploadPage() {

    const navigate = useNavigate();

    const [file, setFile] = useState(null);

    const [source, setSource] = useState("SAP");

    const [fileType, setFileType] = useState("fuel");

    const [loading, setLoading] = useState(false);

    const [message, setMessage] = useState("");

    const handleSubmit = async (e) => {

        e.preventDefault();

        if (!file) {
            setMessage("Please select a file");
            return;
        }

        try {

            setLoading(true);

            const formData = new FormData();

            formData.append("file", file);

            formData.append("source", source);

            formData.append("file_type", fileType);

            let endpoint = "";

            if (fileType === "fuel") {
                endpoint = "/upload/fuel/";
            }
            else if (fileType === "procurement") {
                endpoint = "/upload/procurement/";
            }
            else if (fileType === "electricity") {
                endpoint = "/upload/electricity/";
            }

            const response = await api.post(
                endpoint,
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }
            );

            setMessage(response.data.message);

            setTimeout(() => {
                navigate("/dashboard");
            }, 1500);

        } catch (error) {

            console.error(error);

            setMessage("Upload failed");
        }
        finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mt-5">

            <div className="card shadow p-4">

                <h2 className="mb-4">
                    ESG File Upload
                </h2>

                <form onSubmit={handleSubmit}>

                    <div className="mb-3">

                        <label className="form-label">
                            Source
                        </label>

                        <select
                            className="form-select"
                            value={source}
                            onChange={(e) => setSource(e.target.value)}
                        >
                            <option value="SAP">SAP</option>
                            <option value="Utilitye">Utility</option>
                        </select>

                    </div>

                    <div className="mb-3">

                        <label className="form-label">
                            File Type
                        </label>

                        <select
                            className="form-select"
                            value={fileType}
                            onChange={(e) => setFileType(e.target.value)}
                        >
                            <option value="fuel">Fuel</option>

                            <option value="procurement">
                                Procurement
                            </option>

                            <option value="electricity">
                                Electricity
                            </option>
                        </select>

                    </div>

                    <div className="mb-3">

                        <label className="form-label">
                            CSV File
                        </label>

                        <input
                            type="file"
                            className="form-control"
                            accept=".csv"
                            onChange={(e) => setFile(e.target.files[0])}
                        />

                    </div>

                    <button
                        className="btn btn-primary"
                        disabled={loading}
                    >
                        {
                            loading
                            ? "Uploading..."
                            : "Upload File"
                        }
                    </button>

                </form>

                {
                    message && (
                        <div className="alert alert-info mt-4">
                            {message}
                        </div>
                    )
                }

            </div>

        </div>
    );
}