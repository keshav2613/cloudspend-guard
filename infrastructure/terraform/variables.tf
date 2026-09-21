variable "aws_region" {
  description = "AWS region used by CloudSpend Guard"
  type        = string
  default     = "eu-west-1"
}

variable "project_name" {
  description = "Project name used for AWS resources"
  type        = string
  default     = "cloudspend-guard"
}