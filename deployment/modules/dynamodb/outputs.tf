output "users_table_name" {
  description = "Name of the users DynamoDB table"
  value       = aws_dynamodb_table.users.name
}

output "wardrobe_items_table_name" {
  description = "Name of the wardrobe items DynamoDB table"
  value       = aws_dynamodb_table.wardrobe_items.name
}

output "interactions_table_name" {
  description = "Name of the interactions DynamoDB table"
  value       = aws_dynamodb_table.interactions.name
}

output "rate_limits_table_name" {
  description = "Name of the rate limits DynamoDB table"
  value       = aws_dynamodb_table.rate_limits.name
} 