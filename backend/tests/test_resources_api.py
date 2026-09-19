from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.api.routes.resources.EBSScanner")
def test_list_ebs_resources(mock_scanner_class) -> None:
    mock_scanner = mock_scanner_class.return_value

    mock_scanner.list_volumes.return_value = [
        {
            "volume_id": "vol-0123456789abcdef0",
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

    response = client.get("/api/v1/resources/ebs")

    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["resources"][0]["attached"] is False

@patch("app.api.routes.resources.EC2Scanner")
def test_list_ec2_resources(mock_scanner_class) -> None:
    mock_scanner = mock_scanner_class.return_value

    mock_scanner.list_instances.return_value = [
        {
            "instance_id": "i-0123456789abcdef0",
            "instance_type": "t3.micro",
            "state": "running",
            "availability_zone": "eu-west-1a",
            "private_ip": "10.0.1.10",
            "public_ip": None,
            "name": "dev-server",
        }
    ]

    response = client.get("/api/v1/resources/ec2")

    assert response.status_code == 200

    assert response.json() == {
        "count": 1,
        "resources": [
            {
                "instance_id": "i-0123456789abcdef0",
                "instance_type": "t3.micro",
                "state": "running",
                "availability_zone": "eu-west-1a",
                "private_ip": "10.0.1.10",
                "public_ip": None,
                "name": "dev-server",
            }
        ],
    }

@patch("app.api.routes.recommendations.EBSScanner")
def test_recommendations_endpoint(mock_scanner_class) -> None:
    mock_scanner = mock_scanner_class.return_value

    mock_scanner.list_volumes.return_value = [
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

    response = client.get("/api/v1/recommendations")

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 1
    assert data["recommendations"][0]["resource_id"] == "vol-unused123"
    assert (
        data["recommendations"][0]["finding_type"]
        == "UNATTACHED_EBS_VOLUME"
    )
    
@patch("app.api.routes.recommendations.CloudWatchService")
@patch("app.api.routes.recommendations.EC2Scanner")
@patch("app.api.routes.recommendations.EBSScanner")
def test_recommendations_endpoint_with_low_cpu_ec2(
    mock_ebs_scanner_class,
    mock_ec2_scanner_class,
    mock_cloudwatch_class,
) -> None:
    mock_ebs_scanner_class.return_value.list_volumes.return_value = []

    mock_ec2_scanner_class.return_value.list_instances.return_value = [
        {
            "instance_id": "i-lowcpu123",
            "name": "dev-server",
            "instance_type": "t3.micro",
            "state": "running",
            "availability_zone": "eu-west-1a",
            "private_ip": "10.0.1.10",
            "public_ip": None,
        }
    ]

    mock_cloudwatch_class.return_value.get_average_cpu_utilization.return_value = 2.4

    response = client.get("/api/v1/recommendations")

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 1
    assert data["recommendations"][0]["resource_id"] == "i-lowcpu123"
    assert (
        data["recommendations"][0]["finding_type"]
        == "LOW_EC2_CPU_UTILIZATION"
    )
    assert (
        data["recommendations"][0]["metrics"]["average_cpu_percent"]
        == 2.4
    )