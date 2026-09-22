variable "create_demo_resources" {
  description = "Create intentionally unused AWS resources for CloudSpend Guard portfolio demonstrations"
  type        = bool
  default     = false
}

resource "aws_ebs_volume" "portfolio_demo_1" {
  count = var.create_demo_resources ? 1 : 0

  availability_zone = "eu-west-1a"
  size              = 1
  type              = "gp3"

  tags = {
    Name        = "cloudspend-demo-unused-volume-01"
    Project     = "CloudSpendGuard"
    Environment = "demo"
    Purpose     = "PortfolioDemo"
    ManagedBy   = "Terraform"
  }
}

resource "aws_ebs_volume" "portfolio_demo_2" {
  count = var.create_demo_resources ? 1 : 0

  availability_zone = "eu-west-1b"
  size              = 2
  type              = "gp3"

  tags = {
    Name        = "cloudspend-demo-unused-volume-02"
    Project     = "CloudSpendGuard"
    Environment = "demo"
    Purpose     = "PortfolioDemo"
    ManagedBy   = "Terraform"
  }
}