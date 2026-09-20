import time
from typing import Any

from app.services.aws.cloudwatch import CloudWatchService
from app.services.aws.ebs import EBSScanner
from app.services.aws.ec2 import EC2Scanner
from app.services.aws.pricing import AWSPricingClient
from app.services.pricing import PricingService
from app.services.recommendations import RecommendationEngine


class CloudAnalysisService:
    _cache: dict[str, Any] | None = None
    _cache_created_at: float | None = None

    CACHE_TTL_SECONDS = 60

    def analyze(
        self,
        force_refresh: bool = False,
    ) -> dict[str, Any]:
        if (
            not force_refresh
            and self._cache_is_valid()
        ):
            return self._cache  # type: ignore[return-value]

        result = self._perform_analysis()

        CloudAnalysisService._cache = result
        CloudAnalysisService._cache_created_at = (
            time.monotonic()
        )

        return result

    @classmethod
    def _cache_is_valid(cls) -> bool:
        if (
            cls._cache is None
            or cls._cache_created_at is None
        ):
            return False

        cache_age = (
            time.monotonic()
            - cls._cache_created_at
        )

        return cache_age < cls.CACHE_TTL_SECONDS

    def _perform_analysis(self) -> dict[str, Any]:
        ec2_instances = EC2Scanner().list_instances()
        ebs_volumes = EBSScanner().list_volumes()

        engine = RecommendationEngine()
        cloudwatch = CloudWatchService()
        pricing_client = AWSPricingClient()
        pricing_service = PricingService()

        recommendations: list[dict[str, Any]] = []

        ebs_recommendations = (
            engine.analyze_ebs_volumes(
                ebs_volumes
            )
        )

        for recommendation in ebs_recommendations:
            volume = next(
                (
                    item
                    for item in ebs_volumes
                    if item["volume_id"]
                    == recommendation["resource_id"]
                ),
                None,
            )

            if volume is not None:
                price_per_gb = (
                    pricing_client
                    .get_ebs_price_per_gb_month(
                        volume["volume_type"]
                    )
                )

                if price_per_gb is not None:
                    monthly_cost = (
                        pricing_service
                        .estimate_ebs_monthly_cost(
                            volume,
                            price_per_gb,
                        )
                    )

                    recommendation[
                        "estimated_monthly_cost_usd"
                    ] = float(monthly_cost)

                    recommendation[
                        "potential_monthly_savings_usd"
                    ] = float(monthly_cost)

            recommendations.append(
                recommendation
            )

        for instance in ec2_instances:
            if instance["state"] != "running":
                continue

            cpu_history = (
                cloudwatch
                .get_cpu_utilization_history(
                    instance["instance_id"],
                    days=7,
                )
            )

            if cpu_history:
                average_cpu = round(
                    sum(
                        datapoint[
                            "average_cpu_percent"
                        ]
                        for datapoint in cpu_history
                    )
                    / len(cpu_history),
                    2,
                )
            else:
                average_cpu = None

            recommendation = (
                engine.analyze_ec2_instance(
                    instance,
                    average_cpu,
                )
            )

            if recommendation is not None:
                recommendation[
                    "cpu_history"
                ] = cpu_history

                recommendations.append(
                    recommendation
                )

        low_utilization_ec2 = sum(
            1
            for recommendation in recommendations
            if recommendation["finding_type"]
            == "LOW_EC2_CPU_UTILIZATION"
        )

        unattached_ebs = sum(
            1
            for recommendation in recommendations
            if recommendation["finding_type"]
            == "UNATTACHED_EBS_VOLUME"
        )

        estimated_monthly_savings = sum(
            recommendation.get(
                "potential_monthly_savings_usd",
                0.0,
            )
            for recommendation in recommendations
        )

        summary = {
            "resources": {
                "ec2": len(ec2_instances),
                "ebs": len(ebs_volumes),
                "total": (
                    len(ec2_instances)
                    + len(ebs_volumes)
                ),
            },
            "findings": {
                "total": len(recommendations),
                "low_utilization_ec2": (
                    low_utilization_ec2
                ),
                "unattached_ebs": (
                    unattached_ebs
                ),
            },
            "estimated_monthly_savings_usd": (
                round(
                    estimated_monthly_savings,
                    2,
                )
            ),
        }

        resources = {
            "ec2": ec2_instances,
            "ebs": ebs_volumes,
        }

        return {
            "summary": summary,
            "resources": resources,
            "recommendations": recommendations,
        }