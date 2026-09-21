output "backend_ecr_repository_url" {
  description = "ECR repository URL for the backend"
  value       = aws_ecr_repository.backend.repository_url
}

output "frontend_ecr_repository_url" {
  description = "ECR repository URL for the frontend"
  value       = aws_ecr_repository.frontend.repository_url
}

output "github_actions_role_arn" {
  description = "IAM role assumed by GitHub Actions using OIDC"
  value       = aws_iam_role.github_actions.arn
}

output "vpc_id" {
  description = "CloudSpend Guard VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value = [
    aws_subnet.public_a.id,
    aws_subnet.public_b.id
  ]
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value = [
    aws_subnet.private_a.id,
    aws_subnet.private_b.id
  ]
}

output "nat_gateway_id" {
  description = "NAT Gateway used by private subnets for outbound connectivity"
  value       = aws_nat_gateway.main.id
}

output "eks_cluster_name" {
  description = "Name of the CloudSpend Guard EKS cluster"
  value       = aws_eks_cluster.main.name
}

output "eks_cluster_endpoint" {
  description = "Endpoint of the CloudSpend Guard EKS cluster"
  value       = aws_eks_cluster.main.endpoint
}

output "eks_node_group_name" {
  description = "CloudSpend Guard EKS managed node group"
  value       = aws_eks_node_group.main.node_group_name
}