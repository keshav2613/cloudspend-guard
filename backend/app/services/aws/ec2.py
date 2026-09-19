from typing import Any

import boto3

from app.core.config import get_settings


class EC2Scanner:
    def __init__(self) -> None:
        settings = get_settings()

        self.client = boto3.client(
            "ec2",
            region_name=settings.aws_region,
        )

    def list_instances(self) -> list[dict[str, Any]]:
        paginator = self.client.get_paginator("describe_instances")

        instances: list[dict[str, Any]] = []

        for page in paginator.paginate():
            for reservation in page.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    instances.append(
                        {
                            "instance_id": instance["InstanceId"],
                            "instance_type": instance["InstanceType"],
                            "state": instance["State"]["Name"],
                            "availability_zone": instance["Placement"][
                                "AvailabilityZone"
                            ],
                            "private_ip": instance.get("PrivateIpAddress"),
                            "public_ip": instance.get("PublicIpAddress"),
                            "name": self._get_name(instance.get("Tags", [])),
                        }
                    )

        return instances

    @staticmethod
    def _get_name(tags: list[dict[str, str]]) -> str | None:
        for tag in tags:
            if tag.get("Key") == "Name":
                return tag.get("Value")

        return None