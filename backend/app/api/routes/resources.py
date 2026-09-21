from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
from fastapi import APIRouter, HTTPException

from app.services.aws.ebs import EBSScanner
from app.services.aws.ec2 import EC2Scanner

router = APIRouter(prefix="/resources", tags=["Resources"])


@router.get("/ebs")
async def list_ebs_volumes() -> dict:
    try:
        scanner = EBSScanner()
        volumes = scanner.list_volumes()

        return {
            "count": len(volumes),
            "resources": volumes,
        }

    except NoCredentialsError as exc:
        raise HTTPException(
            status_code=503,
            detail="AWS credentials are not configured.",
        ) from exc

    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve EBS resources from AWS.",
        ) from exc

@router.get("/ec2")
async def list_ec2_instances() -> dict:
    try:
        scanner = EC2Scanner()
        instances = scanner.list_instances()

        return {
            "count": len(instances),
            "resources": instances,
        }

    except NoCredentialsError as exc:
        raise HTTPException(
            status_code=503,
            detail="AWS credentials are not configured.",
        ) from exc

    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve EC2 resources from AWS.",
        ) from exc