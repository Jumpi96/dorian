resource "aws_dynamodb_table" "users" {
  name           = "${var.environment}-users"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "userId"
  stream_enabled = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "userId"
    type = "S"
  }

  tags = var.tags
}

resource "aws_dynamodb_table" "wardrobe_items" {
  name           = "${var.environment}-wardrobe-items"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "userId"
  range_key      = "itemId"
  stream_enabled = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "userId"
    type = "S"
  }

  attribute {
    name = "itemId"
    type = "S"
  }

  global_secondary_index {
    name               = "UserIdIndex"
    hash_key           = "userId"
    projection_type    = "ALL"
  }

  tags = var.tags
}

resource "aws_dynamodb_table" "interactions" {
  name           = "${var.environment}-interactions"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "userId"
  range_key      = "interactionId"
  stream_enabled = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "userId"
    type = "S"
  }

  attribute {
    name = "interactionId"
    type = "S"
  }

  global_secondary_index {
    name               = "UserIdIndex"
    hash_key           = "userId"
    projection_type    = "ALL"
  }

  tags = var.tags
}

resource "aws_dynamodb_table" "rate_limits" {
  name           = "${var.environment}-rate-limits"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "userId"
  range_key      = "date"
  stream_enabled = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "userId"
    type = "S"
  }

  attribute {
    name = "date"
    type = "S"
  }

  global_secondary_index {
    name               = "UserIdIndex"
    hash_key           = "userId"
    projection_type    = "ALL"
  }

  tags = var.tags
} 