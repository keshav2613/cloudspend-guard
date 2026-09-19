from fastapi import APIRouter, HTTPException
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError

from app.services.aws.ebs import EBSScanner
from app.services.recommendations import RecommendationEngine


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.get("")
async def list_recommendations() -> dict:
    try:
        volumes = EBSScanner().list_volumes()

        engine = RecommendationEngine()
        recommendations = engine.analyze_ebs_volumes(volumes)

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