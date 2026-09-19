from app.services.recommendations import RecommendationEngine


def test_low_cpu_instance_creates_recommendation() -> None:
    instance = {
        "instance_id": "i-lowcpu123",
        "name": "dev-server",
        "instance_type": "t3.micro",
        "state": "running",
    }

    engine = RecommendationEngine()

    recommendation = engine.analyze_ec2_instance(
        instance,
        average_cpu=2.4,
    )

    assert recommendation is not None
    assert recommendation["finding_type"] == "LOW_EC2_CPU_UTILIZATION"
    assert recommendation["metrics"]["average_cpu_percent"] == 2.4


def test_normal_cpu_instance_does_not_create_recommendation() -> None:
    instance = {
        "instance_id": "i-active123",
        "name": "production-server",
        "instance_type": "t3.micro",
        "state": "running",
    }

    engine = RecommendationEngine()

    recommendation = engine.analyze_ec2_instance(
        instance,
        average_cpu=27.5,
    )

    assert recommendation is None


def test_instance_without_metrics_does_not_create_recommendation() -> None:
    instance = {
        "instance_id": "i-nodata123",
        "name": "new-server",
        "instance_type": "t3.micro",
        "state": "running",
    }

    engine = RecommendationEngine()

    recommendation = engine.analyze_ec2_instance(
        instance,
        average_cpu=None,
    )

    assert recommendation is None