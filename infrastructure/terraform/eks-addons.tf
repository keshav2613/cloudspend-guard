# ---------------------------------------------------------
# EKS Managed Add-ons
# ---------------------------------------------------------

resource "aws_eks_addon" "vpc_cni" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "vpc-cni"

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-vpc-cni"
  })

  depends_on = [
    aws_eks_node_group.main
  ]
}

resource "aws_eks_addon" "coredns" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "coredns"

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-coredns"
  })

  depends_on = [
    aws_eks_node_group.main
  ]
}

resource "aws_eks_addon" "kube_proxy" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "kube-proxy"

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-kube-proxy"
  })

  depends_on = [
    aws_eks_node_group.main
  ]
}