from decimal import Decimal

from app.services.pricing import PricingService


def test_estimate_ebs_monthly_cost() -> None:
    volume = {
        "volume_id": "vol-test123",
        "volume_type": "gp3",
        "size_gb": 100,
    }

    service = PricingService()

    cost = service.estimate_ebs_monthly_cost(
        volume,
        Decimal("0.08"),
    )

    assert cost == Decimal("8.00")


def test_estimate_ebs_monthly_cost_rounds_to_two_decimals() -> None:
    volume = {
        "volume_id": "vol-test123",
        "volume_type": "gp3",
        "size_gb": 17,
    }

    service = PricingService()

    cost = service.estimate_ebs_monthly_cost(
        volume,
        Decimal("0.083"),
    )

    assert cost == Decimal("1.41")