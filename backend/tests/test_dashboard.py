from decimal import Decimal
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch("app.api.routes.dashboard.AWSPricingClient")
@patch("app.api.routes.dashboard.CloudWatchService")
@patch("app.api.routes.dashboard.EBSScanner")
@patch("app.api.routes.dashboard.EC2Scanner")
def test_dashboard_summary(
    mock_ec2_scanner_class,
    mock_ebs_scanner_class,
    mock_cloudwatch_class,
    mock_pricing_client_class,
) -> None:
    mock_ec2_scanner_class.return_value.list_instances.return_value = [
        {
            "instance_id": "i-lowcpu123",
            "name": "Test instance",
            "instance_type": "t3.micro",
            "state": "running",
            "availability_zone": "eu-west-1a",
            "private_ip": "10.0.1.10",
            "public_ip": None,
        },
        {
            "instance_id": "i-stopped123",
            "name": "Stopped instance",
            "instance_type": "t3.micro",
            "state": "stopped",
            "availability_zone": "eu-west-1a",
            "private_ip": None,
            "public_ip": None,
        },
    ]

    mock_ebs_scanner_class.return_value.list_volumes.return_value = [
        {
            "volume_id": "vol-unused123",
            "name": "old-project-volume",
            "volume_type": "gp3",
            "size_gb": 100,
            "state": "available",
            "availability_zone": "eu-west-1a",
            "encrypted": True,
            "attached": False,
            "attached_instance_ids": [],
        }
    ]

    mock_cloudwatch_class.return_value.get_average_cpu_utilization.return_value = (
        0.12
    )

    mock_pricing_client_class.return_value.get_ebs_price_per_gb_month.return_value = (
        Decimal("0.08")
    )

    response = client.get("/api/v1/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["resources"]["ec2"] == 2
    assert data["resources"]["ebs"] == 1
    assert data["resources"]["total"] == 3

    assert data["findings"]["total"] == 2
    assert data["findings"]["low_utilization_ec2"] == 1
    assert data["findings"]["unattached_ebs"] == 1

    assert data["estimated_monthly_savings_usd"] == 8.0