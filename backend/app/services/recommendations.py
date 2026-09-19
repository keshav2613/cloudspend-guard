from typing import Any


class RecommendationEngine:
    def analyze_ebs_volumes(
        self,
        volumes: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        recommendations: list[dict[str, Any]] = []

        for volume in volumes:
            if volume["state"] == "available" and not volume["attached"]:
                recommendations.append(
                    {
                        "resource_id": volume["volume_id"],
                        "resource_name": volume.get("name"),
                        "resource_type": "EBS",
                        "finding_type": "UNATTACHED_EBS_VOLUME",
                        "severity": "medium",
                        "message": (
                            "EBS volume is currently unattached and "
                            "may be generating unnecessary storage costs."
                        ),
                        "recommendation": (
                            "Review the volume and delete it if it is no longer required."
                        ),
                    }
                )

        return recommendations