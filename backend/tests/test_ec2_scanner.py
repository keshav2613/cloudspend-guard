from unittest.mock import MagicMock, patch

from app.services.aws.ec2 import EC2Scanner


@patch("app.services.aws.ec2.boto3.Session")
def test_list_instances(mock_session_class: MagicMock) -> None:
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session

    mock_ec2 = MagicMock()
    mock_session.client.return_value = mock_ec2

    mock_paginator = MagicMock()
    mock_ec2.get_paginator.return_value = mock_paginator

    mock_paginator.paginate.return_value = [
        {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "InstanceId": "i-0123456789abcdef0",
                            "InstanceType": "t3.micro",
                            "State": {"Name": "running"},
                            "Placement": {
                                "AvailabilityZone": "eu-west-1a"
                            },
                            "PrivateIpAddress": "10.0.1.10",
                            "PublicIpAddress": "203.0.113.10",
                            "Tags": [
                                {
                                    "Key": "Name",
                                    "Value": "cloudspend-test",
                                }
                            ],
                        }
                    ]
                }
            ]
        }
    ]

    scanner = EC2Scanner()
    instances = scanner.list_instances()

    assert len(instances) == 1

    assert instances[0] == {
        "instance_id": "i-0123456789abcdef0",
        "instance_type": "t3.micro",
        "state": "running",
        "availability_zone": "eu-west-1a",
        "private_ip": "10.0.1.10",
        "public_ip": "203.0.113.10",
        "name": "cloudspend-test",
    }

    mock_ec2.get_paginator.assert_called_once_with(
        "describe_instances"
    )