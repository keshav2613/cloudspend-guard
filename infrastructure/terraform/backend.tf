terraform {
  backend "s3" {
    bucket       = "cloudspend-guard-tfstate-216989097516"
    key          = "cloudspend-guard/terraform.tfstate"
    region       = "eu-west-1"
    encrypt      = true
    use_lockfile = true
  }
}