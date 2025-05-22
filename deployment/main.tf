module "dynamodb" {
  source = "./modules/dynamodb"

  environment = var.environment
  tags = {
    Environment = var.environment
    Project     = "dorian"
    ManagedBy   = "terraform"
  }
}

module "lambda" {
  source = "./modules/lambda"

  environment          = var.environment
  google_client_id     = var.google_client_id
  google_client_secret = var.google_client_secret
  jwt_secret_key       = var.jwt_secret_key
  openai_api_key       = var.openai_api_key
} 