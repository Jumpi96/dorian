data "aws_iam_policy" "dynamodb_access" {
  name = "${var.environment}-dynamodb-access"
} 