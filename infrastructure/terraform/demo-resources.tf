# Portfolio demo resources for CloudSpend Guard.
# Intentionally unattached so the application can detect
# and recommend cleanup of unused EBS storage.

resource "aws_ebs_volume" "portfolio_demo_1" {
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