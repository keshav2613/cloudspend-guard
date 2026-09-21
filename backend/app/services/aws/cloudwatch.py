from datetime import UTC, datetime, timedelta

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

    def get_cpu_utilization_history(
        self,
        instance_id: str,
        days: int = 7,
    ) -> list[dict]:
        end_time = datetime.now(UTC)
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

        datapoints = response.get(
            "Datapoints",
            [],
        )

        datapoints.sort(
            key=lambda item: item["Timestamp"]
        )

        return [
            {
                "timestamp": datapoint[
                    "Timestamp"
                ].isoformat(),
                "average_cpu_percent": round(
                    datapoint["Average"],
                    2,
                ),
            }
            for datapoint in datapoints
        ]

    def get_average_cpu_utilization(
        self,
        instance_id: str,
        days: int = 7,
    ) -> float | None:
        history = (
            self.get_cpu_utilization_history(
                instance_id,
                days,
            )
        )

        if not history:
            return None

        average_cpu = sum(
            datapoint[
                "average_cpu_percent"
            ]
            for datapoint in history
        ) / len(history)

        return round(
            average_cpu,
            2,
        )