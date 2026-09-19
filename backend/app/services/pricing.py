from decimal import Decimal, ROUND_HALF_UP
from typing import Any


class PricingService:
    def estimate_ebs_monthly_cost(
        self,
        volume: dict[str, Any],
        price_per_gb_month: Decimal,
    ) -> Decimal:
        size_gb = Decimal(str(volume["size_gb"]))

        estimated_cost = size_gb * price_per_gb_month

        return estimated_cost.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )