from unittest.mock import MagicMock, patch

from app.services.aws.ebs import EBSScanner


@patch("app.services.aws.ebs.boto3.Session")
def test_list_volumes(mock_session_class: MagicMock) -> None:
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session

    mock_ec2 = MagicMock()
    mock_session.client.return_value = mock_ec2

    mock_paginator = MagicMock()
    mock_ec2.get_paginator.return_value = mock_paginator

    mock_paginator.paginate.return_value = [
        {
            "Volumes": [
                {
                    "VolumeId": "vol-0123456789abcdef0",
                    "VolumeType": "gp3",
                    "Size": 100,
                    "State": "available",
                    "AvailabilityZone": "eu-west-1a",
                    "Encrypted": True,
                    "Attachments": [],
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": "old-project-volume",
                        }
                    ],
                }
            ]
        }
    ]

    scanner = EBSScanner()
    volumes = scanner.list_volumes()

    assert len(volumes) == 1

    assert volumes[0] == {
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

    mock_ec2.get_paginator.assert_called_once_with("describe_volumes")