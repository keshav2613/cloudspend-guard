from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.api.routes.dashboard.CloudAnalysisService")
def test_dashboard(
    mock_analysis_service_class,
) -> None:
    mock_analysis_service_class.return_value.analyze.return_value = {
        "summary": {
            "resources": {
                "ec2": 2,
                "ebs": 1,
                "total": 3,
            },
            "findings": {
                "total": 2,
                "low_utilization_ec2": 1,
                "unattached_ebs": 1,
            },
            "estimated_monthly_savings_usd": 8.0,
        },
        "recommendations": [
            {
                "resource_id": "i-lowcpu123",
                "resource_name": "Test instance",
                "resource_type": "EC2",
                "finding_type": "LOW_EC2_CPU_UTILIZATION",
                "severity": "medium",
                "metrics": {
                    "average_cpu_percent": 0.12,
                    "period_days": 7,
                },
                "message": (
                    "EC2 instance has had low average CPU utilization "
                    "during the analysis period."
                ),
                "recommendation": (
                    "Review the instance workload and consider "
                    "rightsizing or stopping it if appropriate."
                ),
            },
            {
                "resource_id": "vol-unused123",
                "resource_name": "old-project-volume",
                "resource_type": "EBS",
                "finding_type": "UNATTACHED_EBS_VOLUME",
                "severity": "medium",
                "message": (
                    "EBS volume is currently unattached and may be "
                    "generating unnecessary storage costs."
                ),
                "recommendation": (
                    "Review the volume and delete it if it is no "
                    "longer required."
                ),
                "estimated_monthly_cost_usd": 8.0,
                "potential_monthly_savings_usd": 8.0,
            },
        ],
    }

    response = client.get("/api/v1/dashboard")

    assert response.status_code == 200

    data = response.json()

    assert data["summary"]["resources"]["ec2"] == 2
    assert data["summary"]["resources"]["ebs"] == 1
    assert data["summary"]["resources"]["total"] == 3

    assert data["summary"]["findings"]["total"] == 2
    assert (
        data["summary"]["findings"]["low_utilization_ec2"]
        == 1
    )
    assert (
        data["summary"]["findings"]["unattached_ebs"]
        == 1
    )

    assert (
        data["summary"]["estimated_monthly_savings_usd"]
        == 8.0
    )

    assert len(data["recommendations"]) == 2

    assert (
        data["recommendations"][0]["resource_id"]
        == "i-lowcpu123"
    )

    assert (
        data["recommendations"][0]["metrics"][
            "average_cpu_percent"
        ]
        == 0.12
    )

    assert (
        data["recommendations"][1][
            "potential_monthly_savings_usd"
        ]
        == 8.0
    )

    mock_analysis_service_class.assert_called_once()

    mock_analysis_service_class.return_value.analyze.assert_called_once()