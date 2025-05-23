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
  lambda_package_key   = var.lambda_package_key
}

module "route53" {
  source = "./modules/route53"

  api_domain_name         = module.lambda.api_domain_name
  api_regional_domain_name = module.lambda.api_regional_domain_name
  api_zone_id             = module.lambda.api_zone_id
}

output "api_url" {
  description = "The URL of the API Gateway"
  value       = "https://${module.lambda.api_domain_name}"
} 