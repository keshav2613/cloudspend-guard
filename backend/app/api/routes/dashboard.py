from fastapi import APIRouter, HTTPException
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError

from app.services.aws.cloudwatch import CloudWatchService
from app.services.aws.ebs import EBSScanner
from app.services.aws.ec2 import EC2Scanner
from app.services.aws.pricing import AWSPricingClient
from app.services.pricing import PricingService
from app.services.recommendations import RecommendationEngine


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/summary")
async def dashboard_summary() -> dict:
    try:
        ec2_instances = EC2Scanner().list_instances()
        ebs_volumes = EBSScanner().list_volumes()

        engine = RecommendationEngine()

        low_utilization_ec2 = 0
        unattached_ebs = 0
        estimated_monthly_savings = 0.0

        # Analyze EC2
        cloudwatch = CloudWatchService()

        for instance in ec2_instances:
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
                low_utilization_ec2 += 1

        # Analyze EBS
        ebs_recommendations = engine.analyze_ebs_volumes(
            ebs_volumes
        )

        unattached_ebs = len(ebs_recommendations)

        pricing_client = AWSPricingClient()
        pricing_service = PricingService()

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

            if volume is None:
                continue

            price_per_gb = (
                pricing_client.get_ebs_price_per_gb_month(
                    volume["volume_type"]
                )
            )

            if price_per_gb is None:
                continue

            monthly_cost = pricing_service.estimate_ebs_monthly_cost(
                volume,
                price_per_gb,
            )

            estimated_monthly_savings += float(monthly_cost)

        total_findings = (
            low_utilization_ec2 + unattached_ebs
        )

        return {
            "resources": {
                "ec2": len(ec2_instances),
                "ebs": len(ebs_volumes),
                "total": len(ec2_instances) + len(ebs_volumes),
            },
            "findings": {
                "total": total_findings,
                "low_utilization_ec2": low_utilization_ec2,
                "unattached_ebs": unattached_ebs,
            },
            "estimated_monthly_savings_usd": round(
                estimated_monthly_savings,
                2,
            ),
        }

    except NoCredentialsError as exc:
        raise HTTPException(
            status_code=503,
            detail="AWS credentials are not configured.",
        ) from exc

    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to generate dashboard summary.",
        ) from exc