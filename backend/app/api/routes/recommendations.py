from fastapi import APIRouter, HTTPException
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError

from app.services.aws.cloudwatch import CloudWatchService
from app.services.aws.ebs import EBSScanner
from app.services.aws.ec2 import EC2Scanner
from app.services.aws.pricing import AWSPricingClient
from app.services.pricing import PricingService
from app.services.recommendations import RecommendationEngine


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.get("")
async def list_recommendations() -> dict:
    try:
        engine = RecommendationEngine()
        pricing_client = AWSPricingClient()
        pricing_service = PricingService()

        recommendations = []

        # Analyze EBS volumes
        volumes = EBSScanner().list_volumes()

        ebs_recommendations = engine.analyze_ebs_volumes(volumes)

        for recommendation in ebs_recommendations:
            volume = next(
                (
                    item
                    for item in volumes
                    if item["volume_id"]
                    == recommendation["resource_id"]
                ),
                None,
            )

            if volume is not None:
                price_per_gb = (
                    pricing_client.get_ebs_price_per_gb_month(
                        volume["volume_type"]
                    )
                )

                if price_per_gb is not None:
                    monthly_cost = (
                        pricing_service.estimate_ebs_monthly_cost(
                            volume,
                            price_per_gb,
                        )
                    )

                    recommendation["estimated_monthly_cost_usd"] = float(
                        monthly_cost
                    )
                    recommendation["potential_monthly_savings_usd"] = float(
                        monthly_cost
                    )

            recommendations.append(recommendation)

        # Analyze EC2 utilization
        instances = EC2Scanner().list_instances()
        cloudwatch = CloudWatchService()

        for instance in instances:
            if instance["state"] != "running":
                continue

            average_cpu = cloudwatch.get_average_cpu_utilization(
                instance["instance_id"],
                days=7,
            )

            recommendation = engine.analyze_ec2_instance(
                instance,
                average_cpu,
            )

            if recommendation is not None:
                recommendations.append(recommendation)

        return {
            "count": len(recommendations),
            "recommendations": recommendations,
        }

    except NoCredentialsError as exc:
        raise HTTPException(
            status_code=503,
            detail="AWS credentials are not configured.",
        ) from exc

    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to analyze AWS resources.",
        ) from exc