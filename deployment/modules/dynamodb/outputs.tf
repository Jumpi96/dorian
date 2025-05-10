output "wardrobe_items_table_name" {
  description = "Name of the wardrobe items DynamoDB table"
  value       = aws_dynamodb_table.wardrobe_items.name
}

output "wardrobe_items_table_arn" {
  description = "ARN of the wardrobe items DynamoDB table"
  value       = aws_dynamodb_table.wardrobe_items.arn
}

output "interactions_table_name" {
  description = "Name of the interactions DynamoDB table"
  value       = aws_dynamodb_table.interactions.name
}

output "interactions_table_arn" {
  description = "ARN of the interactions DynamoDB table"
  value       = aws_dynamodb_table.interactions.arn
}

output "rate_limits_table_name" {
  description = "Name of the rate limits DynamoDB table"
  value       = aws_dynamodb_table.rate_limits.name
}

output "rate_limits_table_arn" {
  description = "ARN of the rate limits DynamoDB table"
  value       = aws_dynamodb_table.rate_limits.arn
} 