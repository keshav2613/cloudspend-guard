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
                            "Review the volume and delete it if it is "
                            "no longer required."
                        ),
                    }
                )

        return recommendations

    def analyze_ec2_instance(
        self,
        instance: dict[str, Any],
        average_cpu: float | None,
    ) -> dict[str, Any] | None:
        if instance["state"] != "running":
            return None

        if average_cpu is None:
            return None

        if average_cpu >= 5.0:
            return None

        return {
            "resource_id": instance["instance_id"],
            "resource_name": instance.get("name"),
            "resource_type": "EC2",
            "finding_type": "LOW_EC2_CPU_UTILIZATION",
            "severity": "medium",
            "metrics": {
                "average_cpu_percent": average_cpu,
                "period_days": 7,
            },
            "message": (
                "EC2 instance has had low average CPU utilization "
                "during the analysis period."
            ),
            "recommendation": (
                "Review the instance workload and consider rightsizing "
                "or stopping it if appropriate."
            ),
        }