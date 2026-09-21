output "backend_ecr_repository_url" {
  description = "ECR repository URL for the backend"
  value       = aws_ecr_repository.backend.repository_url
}

output "frontend_ecr_repository_url" {
  description = "ECR repository URL for the frontend"
  value       = aws_ecr_repository.frontend.repository_url
}