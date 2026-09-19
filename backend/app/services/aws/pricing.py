import json
from decimal import Decimal

import boto3

from app.core.config import get_settings


class AWSPricingClient:
    def __init__(self) -> None:
        settings = get_settings()

        session = boto3.Session(
            profile_name=settings.aws_profile,
            region_name="us-east-1",
        )

        self.client = session.client("pricing")

    def get_ebs_price_per_gb_month(
        self,
        volume_type: str,
        location: str = "EU (Ireland)",
    ) -> Decimal | None:
        supported_volume_types = {
            "gp2",
            "gp3",
        }

        if volume_type not in supported_volume_types:
            return None

        response = self.client.get_products(
            ServiceCode="AmazonEC2",
            Filters=[
                {
                    "Type": "TERM_MATCH",
                    "Field": "location",
                    "Value": location,
                },
                {
                    "Type": "TERM_MATCH",
                    "Field": "volumeApiName",
                    "Value": volume_type,
                },
            ],
            MaxResults=100,
        )

        for product_json in response.get("PriceList", []):
            product = json.loads(product_json)

            terms = product.get("terms", {}).get("OnDemand", {})

            for term in terms.values():
                for dimension in term.get(
                    "priceDimensions",
                    {}
                ).values():
                    if dimension.get("unit") != "GB-Mo":
                        continue

                    usd_price = dimension.get(
                        "pricePerUnit",
                        {},
                    ).get("USD")

                    if usd_price is not None:
                        return Decimal(usd_price)

        return None