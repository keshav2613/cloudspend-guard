from fastapi import APIRouter, HTTPException
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError

from app.services.aws.cloudwatch import CloudWatchService
from app.services.aws.ebs import EBSScanner
from app.services.aws.ec2 import EC2Scanner
from app.services.recommendations import RecommendationEngine


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.get("")
async def list_recommendations() -> dict:
    try:
        engine = RecommendationEngine()
        recommendations = []

        # Analyze EBS volumes
        volumes = EBSScanner().list_volumes()
        recommendations.extend(
            engine.analyze_ebs_volumes(volumes)
        )

        # Analyze EC2 instances using CloudWatch metrics
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