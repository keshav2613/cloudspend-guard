# ---------------------------------------------------------
# EKS Pod Identity Agent
# ---------------------------------------------------------

resource "aws_eks_addon" "pod_identity_agent" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "eks-pod-identity-agent"

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-pod-identity-agent"
  })

  depends_on = [
    aws_eks_node_group.main
  ]
}


# ---------------------------------------------------------
# CloudSpend Guard Backend IAM Role
# ---------------------------------------------------------

data "aws_iam_policy_document" "backend_pod_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["pods.eks.amazonaws.com"]
    }

    actions = [
      "sts:AssumeRole",
      "sts:TagSession"
    ]
  }
}

resource "aws_iam_role" "backend_pod" {
  name               = "${var.project_name}-backend-pod-role"
  assume_role_policy = data.aws_iam_policy_document.backend_pod_assume_role.json

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-backend-pod-role"
  })
}


# ---------------------------------------------------------
# Least-Privilege Backend AWS Permissions
# ---------------------------------------------------------

data "aws_iam_policy_document" "backend_aws_access" {

  statement {
    sid    = "ReadEC2Resources"
    effect = "Allow"

    actions = [
      "ec2:DescribeInstances",
      "ec2:DescribeVolumes"
    ]

    resources = ["*"]
  }

  statement {
    sid    = "ReadCloudWatchMetrics"
    effect = "Allow"

    actions = [
      "cloudwatch:GetMetricData",
      "cloudwatch:GetMetricStatistics"
    ]

    resources = ["*"]
  }

  statement {
    sid    = "ReadPricing"
    effect = "Allow"

    actions = [
      "pricing:GetProducts"
    ]

    resources = ["*"]
  }
}

resource "aws_iam_policy" "backend_aws_access" {
  name        = "${var.project_name}-backend-aws-access"
  description = "Read-only AWS permissions required by CloudSpend Guard backend"
  policy      = data.aws_iam_policy_document.backend_aws_access.json

  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "backend_aws_access" {
  role       = aws_iam_role.backend_pod.name
  policy_arn = aws_iam_policy.backend_aws_access.arn
}