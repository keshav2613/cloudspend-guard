data "tls_certificate" "github_actions" {
  url = "https://token.actions.githubusercontent.com"
}

resource "aws_iam_openid_connect_provider" "github_actions" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = [
    "sts.amazonaws.com"
  ]

  thumbprint_list = [
    data.tls_certificate.github_actions.certificates[0].sha1_fingerprint
  ]

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}

data "aws_iam_policy_document" "github_actions_assume_role" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRoleWithWebIdentity"
    ]

    principals {
      type = "Federated"

      identifiers = [
        aws_iam_openid_connect_provider.github_actions.arn
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"

      values = [
        "sts.amazonaws.com"
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"

      values = [
        "repo:keshav2613@76985675/cloudspend-guard@1375665471:ref:refs/heads/main"
      ]
    }
  }
}

resource "aws_iam_role" "github_actions" {
  name = "${var.project_name}-github-actions"

  assume_role_policy = data.aws_iam_policy_document.github_actions_assume_role.json

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}

data "aws_iam_policy_document" "github_actions_ecr" {
  statement {
    sid    = "ECRAuthentication"
    effect = "Allow"

    actions = [
      "ecr:GetAuthorizationToken"
    ]

    resources = ["*"]
  }

  statement {
    sid    = "PushCloudSpendImages"
    effect = "Allow"

    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:CompleteLayerUpload",
      "ecr:GetDownloadUrlForLayer",
      "ecr:InitiateLayerUpload",
      "ecr:PutImage",
      "ecr:UploadLayerPart"
    ]

    resources = [
      aws_ecr_repository.backend.arn,
      aws_ecr_repository.frontend.arn
    ]
  }
}

resource "aws_iam_role_policy" "github_actions_ecr" {
  name = "${var.project_name}-ecr-push"

  role   = aws_iam_role.github_actions.id
  policy = data.aws_iam_policy_document.github_actions_ecr.json
}