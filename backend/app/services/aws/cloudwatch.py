from datetime import datetime, timedelta, timezone

import boto3

from app.core.config import get_settings


class CloudWatchService:
    def __init__(self) -> None:
        settings = get_settings()

        session = boto3.Session(
            profile_name=settings.aws_profile,
            region_name=settings.aws_region,
        )

        self.client = session.client("cloudwatch")

    def get_average_cpu_utilization(
        self,
        instance_id: str,
        days: int = 7,
    ) -> float | None:
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=days)

        response = self.client.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[
                {
                    "Name": "InstanceId",
                    "Value": instance_id,
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=["Average"],
        )

        datapoints = response.get("Datapoints", [])

        if not datapoints:
            return None

        average_cpu = sum(
            datapoint["Average"] for datapoint in datapoints
        ) / len(datapoints)

        return round(average_cpu, 2)