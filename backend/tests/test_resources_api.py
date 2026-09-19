from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


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