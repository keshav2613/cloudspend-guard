from unittest.mock import MagicMock, patch

from app.services.aws.cloudwatch import CloudWatchService


@patch("app.services.aws.cloudwatch.boto3.Session")
def test_get_average_cpu_utilization(
    mock_session_class: MagicMock,
) -> None:
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session

    mock_cloudwatch = MagicMock()
    mock_session.client.return_value = mock_cloudwatch

    mock_cloudwatch.get_metric_statistics.return_value = {
        "Datapoints": [
            {"Average": 2.0},
            {"Average": 4.0},
            {"Average": 3.0},
        ]
    }

    service = CloudWatchService()

    average_cpu = service.get_average_cpu_utilization(
        "i-0123456789abcdef0"
    )

    assert average_cpu == 3.0

    mock_session.client.assert_called_once_with("cloudwatch")
    mock_cloudwatch.get_metric_statistics.assert_called_once()


@patch("app.services.aws.cloudwatch.boto3.Session")
def test_get_average_cpu_utilization_without_data(
    mock_session_class: MagicMock,
) -> None:
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session

    mock_cloudwatch = MagicMock()
    mock_session.client.return_value = mock_cloudwatch

    mock_cloudwatch.get_metric_statistics.return_value = {
        "Datapoints": []
    }

    service = CloudWatchService()

    average_cpu = service.get_average_cpu_utilization(
        "i-0123456789abcdef0"
    )

    assert average_cpu is None