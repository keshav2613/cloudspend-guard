from app.services.recommendations import RecommendationEngine


def test_unattached_ebs_volume_creates_recommendation() -> None:
    volumes = [
        {
            "volume_id": "vol-unused123",
            "name": "old-project-volume",
            "volume_type": "gp3",
            "size_gb": 100,
            "state": "available",
            "availability_zone": "eu-west-1a",
            "encrypted": True,
            "attached": False,
            "attached_instance_ids": [],
        }
    ]

    engine = RecommendationEngine()

    recommendations = engine.analyze_ebs_volumes(volumes)

    assert len(recommendations) == 1
    assert recommendations[0]["resource_id"] == "vol-unused123"
    assert recommendations[0]["finding_type"] == "UNATTACHED_EBS_VOLUME"
    assert recommendations[0]["severity"] == "medium"


def test_attached_ebs_volume_does_not_create_recommendation() -> None:
    volumes = [
        {
            "volume_id": "vol-used123",
            "name": "production-volume",
            "volume_type": "gp3",
            "size_gb": 100,
            "state": "in-use",
            "availability_zone": "eu-west-1a",
            "encrypted": True,
            "attached": True,
            "attached_instance_ids": ["i-123456789"],
        }
    ]

    engine = RecommendationEngine()

    recommendations = engine.analyze_ebs_volumes(volumes)

    assert recommendations == []