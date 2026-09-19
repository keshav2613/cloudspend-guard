import json
from decimal import Decimal
from unittest.mock import MagicMock, patch

from app.services.aws.pricing import AWSPricingClient


@patch("app.services.aws.pricing.boto3.Session")
def test_get_ebs_price_per_gb_month(
    mock_session_class: MagicMock,
) -> None:
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session

    mock_pricing = MagicMock()
    mock_session.client.return_value = mock_pricing

    product = {
        "terms": {
            "OnDemand": {
                "test-term": {
                    "priceDimensions": {
                        "test-dimension": {
                            "unit": "GB-Mo",
                            "pricePerUnit": {
                                "USD": "0.0800000000",
                            },
                        }
                    }
                }
            }
        }
    }

    mock_pricing.get_products.return_value = {
        "PriceList": [json.dumps(product)]
    }

    client = AWSPricingClient()

    price = client.get_ebs_price_per_gb_month("gp3")

    assert price == Decimal("0.0800000000")

    mock_session.client.assert_called_once_with("pricing")
    mock_pricing.get_products.assert_called_once()