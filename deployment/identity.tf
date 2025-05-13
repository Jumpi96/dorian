# IAM User for application access
resource "aws_iam_user" "app_user" {
  name = "${var.environment}-app-user"
  tags = {
    Environment = var.environment
    Project     = "dorian"
    ManagedBy   = "terraform"
  }
}

# IAM Policy for DynamoDB access
resource "aws_iam_policy" "dynamodb_access" {
  name        = "${var.environment}-dynamodb-access"
  description = "Policy for accessing DynamoDB tables"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchGetItem",
          "dynamodb:BatchWriteItem"
        ]
        Resource = [
          module.dynamodb.wardrobe_items_table_arn,
          "${module.dynamodb.wardrobe_items_table_arn}/index/*",
          module.dynamodb.interactions_table_arn,
          "${module.dynamodb.interactions_table_arn}/index/*",
          module.dynamodb.rate_limits_table_arn,
          "${module.dynamodb.rate_limits_table_arn}/index/*",
          module.dynamodb.trips_table_arn,
          "${module.dynamodb.trips_table_arn}/index/*"
        ]
      }
    ]
  })

  tags = {
    Environment = var.environment
    Project     = "dorian"
    ManagedBy   = "terraform"
  }
}

# Attach the policy to the user
resource "aws_iam_user_policy_attachment" "dynamodb_access" {
  user       = aws_iam_user.app_user.name
  policy_arn = aws_iam_policy.dynamodb_access.arn
}
