# ---------------------------------------------------------
# CloudSpend Guard Backend Pod Identity Association
# ---------------------------------------------------------

resource "aws_eks_pod_identity_association" "backend" {
  cluster_name    = aws_eks_cluster.main.name
  namespace       = "cloudspend"
  service_account = "cloudspend-backend"
  role_arn        = aws_iam_role.backend_pod.arn

  depends_on = [
    aws_eks_addon.pod_identity_agent,
    aws_iam_role_policy_attachment.backend_aws_access
  ]

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-backend-pod-identity"
  })
}