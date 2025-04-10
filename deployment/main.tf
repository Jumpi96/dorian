module "dynamodb" {
  source = "./modules/dynamodb"

  environment = var.environment
  tags = {
    Environment = var.environment
    Project     = "dorian"
    ManagedBy   = "terraform"
  }
} 