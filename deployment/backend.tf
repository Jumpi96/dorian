terraform {
  backend "s3" {
    bucket  = "dorian-terraform-state"
    key     = "terraform.tfstate"
    region  = "eu-central-1"
    encrypt = true
  }
} 