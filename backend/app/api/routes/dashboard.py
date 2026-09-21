from botocore.exceptions import (
    BotoCoreError,
    ClientError,
    NoCredentialsError,
)
from fastapi import APIRouter, HTTPException, Query

from app.services.cloud_analysis import CloudAnalysisService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("")
def dashboard(
    refresh: bool = Query(
        default=False,
        description="Bypass cached analysis and fetch fresh AWS data.",
    ),
) -> dict:
    try:
        return CloudAnalysisService().analyze(
            force_refresh=refresh
        )

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