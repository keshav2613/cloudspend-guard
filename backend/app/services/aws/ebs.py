from typing import Any

import boto3

from app.core.config import get_settings


class EBSScanner:
    def __init__(self) -> None:
        settings = get_settings()

        session = boto3.Session(
            profile_name=settings.aws_profile,
            region_name=settings.aws_region,
        )

        self.client = session.client("ec2")

    def list_volumes(self) -> list[dict[str, Any]]:
        paginator = self.client.get_paginator("describe_volumes")

        volumes: list[dict[str, Any]] = []

        for page in paginator.paginate():
            for volume in page.get("Volumes", []):
                attachments = volume.get("Attachments", [])

                volumes.append(
                    {
                        "volume_id": volume["VolumeId"],
                        "name": self._get_name(volume.get("Tags", [])),
                        "volume_type": volume["VolumeType"],
                        "size_gb": volume["Size"],
                        "state": volume["State"],
                        "availability_zone": volume["AvailabilityZone"],
                        "encrypted": volume.get("Encrypted", False),
                        "attached": len(attachments) > 0,
                        "attached_instance_ids": [
                            attachment["InstanceId"]
                            for attachment in attachments
                            if "InstanceId" in attachment
                        ],
                    }
                )

        return volumes

    @staticmethod
    def _get_name(tags: list[dict[str, str]]) -> str | None:
        for tag in tags:
            if tag.get("Key") == "Name":
                return tag.get("Value")

        return None