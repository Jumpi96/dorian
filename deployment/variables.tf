variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "google_client_id" {
  description = "Google OAuth client ID"
  type        = string
  sensitive   = true
}

variable "google_client_secret" {
  description = "Google OAuth client secret"
  type        = string
  sensitive   = true
}

variable "jwt_secret_key" {
  description = "JWT secret key for authentication"
  type        = string
  sensitive   = true
}

variable "openai_api_key" {
  description = "OpenAI API key"
  type        = string
  sensitive   = true
}

variable "frontend_redirect_success" {
  description = "Frontend redirect success URL"
  type        = string
}

variable "lambda_package_key" {
  description = "S3 key for the Lambda deployment package"
  type        = string
}

variable "cookie_domain" {
  description = "Cookie domain"
  type        = string
}