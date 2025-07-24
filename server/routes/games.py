from flask import jsonify, Response, Blueprint, request
from models import db, Game, Publisher, Category
from sqlalchemy.orm import Query
from typing import Optional

# Create a Blueprint for games routes
games_bp = Blueprint('games', __name__)

def get_games_base_query() -> Query:
    """Get the base query for games with publisher and category joins
    
    Returns:
        Query: SQLAlchemy query object with joined tables
    """
    return db.session.query(Game).join(
        Publisher, 
        Game.publisher_id == Publisher.id, 
        isouter=True
    ).join(
        Category, 
        Game.category_id == Category.id, 
        isouter=True
    )

def apply_game_filters(query: Query, category_id: Optional[int] = None, publisher_id: Optional[int] = None) -> Query:
    """Apply filtering to the games query based on category and publisher
    
    Args:
        query: Base SQLAlchemy query object
        category_id: Optional category ID to filter by
        publisher_id: Optional publisher ID to filter by
        
    Returns:
        Query: Filtered SQLAlchemy query object
    """
    if category_id is not None:
        query = query.filter(Game.category_id == category_id)
    
    if publisher_id is not None:
        query = query.filter(Game.publisher_id == publisher_id)
    
    return query

@games_bp.route('/api/games', methods=['GET'])
def get_games() -> Response:
    """Get all games with optional filtering by category and publisher
    
    Query Parameters:
        category_id (int, optional): Filter games by category ID
        publisher_id (int, optional): Filter games by publisher ID
        
    Returns:
        Response: JSON response with list of games
    """
    # Get filter parameters from query string
    category_id = request.args.get('category_id', type=int)
    publisher_id = request.args.get('publisher_id', type=int)
    
    # Use the base query for all games
    games_query = get_games_base_query()
    
    # Apply filters if provided
    games_query = apply_game_filters(games_query, category_id, publisher_id)
    
    # Execute query
    games_result = games_query.all()
    
    # Convert the results using the model's to_dict method
    games_list = [game.to_dict() for game in games_result]
    
    return jsonify(games_list)

@games_bp.route('/api/games/<int:id>', methods=['GET'])
def get_game(id: int) -> tuple[Response, int] | Response:
    # Use the base query and add filter for specific game
    game_query = get_games_base_query().filter(Game.id == id).first()
    
    # Return 404 if game not found
    if not game_query: 
        return jsonify({"error": "Game not found"}), 404
    
    # Convert the result using the model's to_dict method
    game = game_query.to_dict()
    
    return jsonify(game)
