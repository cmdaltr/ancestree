from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, List
import os

from ..database import get_db
from ..models import User, SearchHistory
from ..schemas import SearchQuery, SearchResult
from ..utils.auth import get_current_user
from ..services.genealogy_scraper import GenealogySearchService
from ..services.ai_search import AISearchService

router = APIRouter(prefix="/api/search", tags=["search"])

# Initialize services
genealogy_service = GenealogySearchService(config={
    'ancestry_api_key': os.getenv('ANCESTRY_API_KEY'),
    'familysearch_username': os.getenv('FAMILYSEARCH_USERNAME'),
    'familysearch_password': os.getenv('FAMILYSEARCH_PASSWORD'),
    'findmypast_api_key': os.getenv('FINDMYPAST_API_KEY'),
    'myheritage_api_key': os.getenv('MYHERITAGE_API_KEY')
})

ai_service = AISearchService()

def save_search_history(
    db: Session,
    user_id: int,
    query: Dict,
    search_type: str,
    results_count: int,
    sources: List[str]
):
    """Save search to history"""
    history = SearchHistory(
        user_id=user_id,
        query=str(query),
        search_type=search_type,
        results_count=results_count,
        sources_searched=",".join(sources)
    )
    db.add(history)
    db.commit()

@router.post("/genealogy", response_model=Dict)
async def search_genealogy_records(
    query: SearchQuery,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Search genealogy records across multiple sources.
    If use_ai is True, AI will enhance the query and analyze results.
    """
    # Convert query to dict
    query_dict = {
        'first_name': query.first_name,
        'last_name': query.last_name,
        'birth_year': query.birth_year,
        'birth_place': query.birth_place,
        'death_year': query.death_year,
        'death_place': query.death_place
    }

    # Remove None values
    query_dict = {k: v for k, v in query_dict.items() if v is not None}

    # AI-enhanced search
    if query.use_ai:
        try:
            # Get AI suggestions for search strategy
            strategy = await ai_service.suggest_search_strategy(query_dict)

            # Enhance query with AI
            enhanced_query = await ai_service.enhance_query(query_dict)

            # Use AI-suggested sources if available
            sources = strategy.get('suggested_sources', query.sources)
        except Exception as e:
            print(f"AI enhancement failed: {e}")
            enhanced_query = query_dict
            sources = query.sources
    else:
        enhanced_query = query_dict
        sources = query.sources

    # Search genealogy sources
    results = await genealogy_service.search_all(enhanced_query, sources)

    # Calculate total results
    total_results = sum(len(records) for records in results.values())

    # AI analysis of results
    analysis = None
    if query.use_ai and total_results > 0:
        try:
            analysis = await ai_service.analyze_results(query_dict, results)
        except Exception as e:
            print(f"AI analysis failed: {e}")

    # Save to search history in background
    background_tasks.add_task(
        save_search_history,
        db,
        current_user.id,
        query_dict,
        "ai_assisted" if query.use_ai else "manual",
        total_results,
        sources
    )

    response = {
        "query": query_dict,
        "results": results,
        "total_results": total_results,
        "sources_searched": sources
    }

    if analysis:
        response["ai_analysis"] = analysis

    return response

@router.get("/history")
def get_search_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 50
):
    """Get user's search history"""
    history = db.query(SearchHistory).filter(
        SearchHistory.user_id == current_user.id
    ).order_by(SearchHistory.created_at.desc()).offset(skip).limit(limit).all()

    return history

@router.get("/sources")
def get_available_sources():
    """Get list of available genealogy sources"""
    return {
        "sources": [
            {
                "id": "ancestry",
                "name": "Ancestry.com",
                "requires_auth": True,
                "api_available": True
            },
            {
                "id": "familysearch",
                "name": "FamilySearch",
                "requires_auth": True,
                "api_available": True
            },
            {
                "id": "findmypast",
                "name": "Find My Past",
                "requires_auth": True,
                "api_available": True
            },
            {
                "id": "myheritage",
                "name": "MyHeritage",
                "requires_auth": True,
                "api_available": False
            }
        ]
    }
