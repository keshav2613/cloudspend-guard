from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from app.services.aws.cloudwatch import (
    CloudWatchService,
)


@patch(
    "app.services.aws.cloudwatch.boto3.Session"
)
def test_get_average_cpu_utilization(
    mock_session_class,
) -> None:
    mock_client = MagicMock()

    mock_session_class.return_value.client.return_value = (
        mock_client
    )

    mock_client.get_metric_statistics.return_value = {
        "Datapoints": [
            {
                "Timestamp": datetime(
                    2026,
                    9,
                    18,
                    10,
                    0,
                    tzinfo=timezone.utc,
                ),
                "Average": 2.0,
            },
            {
                "Timestamp": datetime(
                    2026,
                    9,
                    18,
                    11,
                    0,
                    tzinfo=timezone.utc,
                ),
                "Average": 4.0,
            },
            {
                "Timestamp": datetime(
                    2026,
                    9,
                    18,
                    12,
                    0,
                    tzinfo=timezone.utc,
                ),
                "Average": 6.0,
            },
        ]
    }

    service = CloudWatchService()

    result = (
        service.get_average_cpu_utilization(
            "i-test123",
            days=7,
        )
    )

    assert result == 4.0

    mock_client.get_metric_statistics.assert_called_once()
    
@patch(
    "app.services.aws.cloudwatch.boto3.Session"
)
def test_get_cpu_utilization_history(
    mock_session_class,
) -> None:
    mock_client = MagicMock()

    mock_session_class.return_value.client.return_value = (
        mock_client
    )

    mock_client.get_metric_statistics.return_value = {
        "Datapoints": [
            {
                "Timestamp": datetime(
                    2026,
                    9,
                    18,
                    12,
                    0,
                    tzinfo=timezone.utc,
                ),
                "Average": 6.25,
            },
            {
                "Timestamp": datetime(
                    2026,
                    9,
                    18,
                    10,
                    0,
                    tzinfo=timezone.utc,
                ),
                "Average": 2.15,
            },
            {
                "Timestamp": datetime(
                    2026,
                    9,
                    18,
                    11,
                    0,
                    tzinfo=timezone.utc,
                ),
                "Average": 4.35,
            },
        ]
    }

    service = CloudWatchService()

    result = (
        service.get_cpu_utilization_history(
            "i-test123",
            days=7,
        )
    )

    assert len(result) == 3

    assert result[0] == {
        "timestamp": (
            "2026-09-18T10:00:00+00:00"
        ),
        "average_cpu_percent": 2.15,
    }

    assert result[1][
        "average_cpu_percent"
    ] == 4.35

    assert result[2][
        "average_cpu_percent"
    ] == 6.25