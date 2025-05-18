import pytest
from datetime import datetime, UTC
from unittest.mock import Mock, patch
from app.services.interactions import InteractionsService
from app.clients.dynamodb import DynamoDBError

@pytest.fixture
def mock_dynamodb():
    return Mock()

@pytest.fixture
def interactions_service(mock_dynamodb):
    return InteractionsService(mock_dynamodb)

def test_save_recommendation_interaction_success(interactions_service, mock_dynamodb):
    # Arrange
    user_id = "test_user"
    situation = "casual dinner"
    recommendation = {
        "top": "Black t-shirt",
        "bottom": "Blue jeans",
        "shoes": "White sneakers"
    }
    
    # Mock datetime to have a consistent timestamp
    with patch('app.services.interactions.datetime') as mock_datetime:
        mock_now = datetime(2024, 3, 21, 12, 0, 0, tzinfo=UTC)
        mock_datetime.now.return_value = mock_now
        mock_datetime.UTC = UTC
        
        # Act
        interaction_id = interactions_service.save_recommendation_interaction(
            user_id=user_id,
            situation=situation,
            recommendation=recommendation
        )
        
        # Assert
        expected_id = f"rec_{mock_now.isoformat()}"
        assert interaction_id == expected_id
        
        mock_dynamodb.put_item.assert_called_once_with(
            table_name="dev-interactions",
            item={
                "interactionId": expected_id,
                "userId": user_id,
                "type": "outfit_recommendation",
                "situation": situation,
                "recommendation": recommendation,
                "tripId": None,
                "createdAt": mock_now.isoformat()
            }
        )

def test_save_recommendation_interaction_dynamodb_error(interactions_service, mock_dynamodb):
    # Arrange
    user_id = "test_user"
    situation = "casual dinner"
    recommendation = {
        "top": "Black t-shirt",
        "bottom": "Blue jeans",
        "shoes": "White sneakers"
    }
    
    mock_dynamodb.put_item.side_effect = DynamoDBError("Test error")
    
    # Act & Assert
    with pytest.raises(DynamoDBError) as exc_info:
        interactions_service.save_recommendation_interaction(
            user_id=user_id,
            situation=situation,
            recommendation=recommendation
        )
    
    assert str(exc_info.value) == "Test error"

def test_update_interaction_feedback_success(interactions_service, mock_dynamodb):
    # Arrange
    user_id = "test_user"
    interaction_id = "rec_123"
    feedback = 1  # Positive feedback
    
    # Act
    interactions_service.update_interaction_feedback(user_id, interaction_id, feedback)
    
    # Assert
    mock_dynamodb.update_item.assert_called_once_with(
        table_name="dev-interactions",
        key={
            "userId": user_id,
            "interactionId": interaction_id
        },
        update_expression="SET #feedback = :feedback",
        expression_attribute_names={
            "#feedback": "feedback"
        },
        expression_attribute_values={
            ":feedback": feedback
        }
    )

def test_update_interaction_feedback_negative(interactions_service, mock_dynamodb):
    # Arrange
    user_id = "test_user"
    interaction_id = "rec_123"
    feedback = 0  # Negative feedback
    
    # Act
    interactions_service.update_interaction_feedback(user_id, interaction_id, feedback)
    
    # Assert
    mock_dynamodb.update_item.assert_called_once_with(
        table_name="dev-interactions",
        key={
            "userId": user_id,
            "interactionId": interaction_id
        },
        update_expression="SET #feedback = :feedback",
        expression_attribute_names={
            "#feedback": "feedback"
        },
        expression_attribute_values={
            ":feedback": feedback
        }
    )

def test_update_interaction_feedback_dynamodb_error(interactions_service, mock_dynamodb):
    # Arrange
    user_id = "test_user"
    interaction_id = "rec_123"
    feedback = 1
    
    mock_dynamodb.update_item.side_effect = DynamoDBError("Test error")
    
    # Act & Assert
    with pytest.raises(DynamoDBError) as exc_info:
        interactions_service.update_interaction_feedback(user_id, interaction_id, feedback)
    
    assert str(exc_info.value) == "Test error" 