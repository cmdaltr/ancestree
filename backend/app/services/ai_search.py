import os
from typing import Dict, List, Optional
import logging
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AISearchService:
    """
    AI-powered search service to intelligently query and analyze genealogy results.
    """

    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None

        # Initialize clients if API keys are available
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai_key != "your-openai-key-here":
            self.openai_client = AsyncOpenAI(api_key=openai_key)

        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key and anthropic_key != "your-anthropic-key-here":
            self.anthropic_client = AsyncAnthropic(api_key=anthropic_key)

    async def enhance_query(self, query: Dict) -> Dict:
        """
        Use AI to enhance and expand search queries with variations.
        """
        if not self._has_ai_client():
            logger.warning("No AI client available")
            return query

        try:
            prompt = self._build_query_enhancement_prompt(query)

            if self.anthropic_client:
                response = await self._query_anthropic(prompt)
            elif self.openai_client:
                response = await self._query_openai(prompt)
            else:
                return query

            # Parse AI response to get enhanced query suggestions
            enhanced = self._parse_enhancement_response(response, query)
            return enhanced

        except Exception as e:
            logger.error(f"Error enhancing query with AI: {e}")
            return query

    async def analyze_results(self, query: Dict, results: Dict[str, List[Dict]]) -> Dict:
        """
        Use AI to analyze search results and find the most likely matches.
        """
        if not self._has_ai_client():
            return {
                "ranked_results": results,
                "confidence_scores": {},
                "recommendations": []
            }

        try:
            prompt = self._build_analysis_prompt(query, results)

            if self.anthropic_client:
                analysis = await self._query_anthropic(prompt)
            elif self.openai_client:
                analysis = await self._query_openai(prompt)
            else:
                return {"ranked_results": results}

            # Parse AI analysis
            parsed = self._parse_analysis_response(analysis, results)
            return parsed

        except Exception as e:
            logger.error(f"Error analyzing results with AI: {e}")
            return {"ranked_results": results}

    async def suggest_search_strategy(self, query: Dict, person_context: Optional[Dict] = None) -> Dict:
        """
        Use AI to suggest optimal search strategies based on available information.
        """
        if not self._has_ai_client():
            return {
                "suggested_sources": ["ancestry", "familysearch", "findmypast", "myheritage"],
                "search_tips": []
            }

        try:
            prompt = f"""Given the following search query for a genealogy search:
{query}

{'And this additional context about the person: ' + str(person_context) if person_context else ''}

Suggest:
1. Which genealogy sources would be most effective (ancestry, familysearch, findmypast, myheritage)
2. What variations of the name should be searched
3. What time periods to focus on
4. Any specific record types that might be most helpful
5. Alternative search strategies if initial search yields no results

Provide a structured JSON response."""

            if self.anthropic_client:
                response = await self._query_anthropic(prompt)
            else:
                response = await self._query_openai(prompt)

            return self._parse_strategy_response(response)

        except Exception as e:
            logger.error(f"Error getting AI search strategy: {e}")
            return {"suggested_sources": ["ancestry", "familysearch"]}

    def _has_ai_client(self) -> bool:
        return self.openai_client is not None or self.anthropic_client is not None

    def _build_query_enhancement_prompt(self, query: Dict) -> str:
        return f"""Analyze this genealogy search query and suggest enhancements:

Query:
- First Name: {query.get('first_name', 'N/A')}
- Last Name: {query.get('last_name', 'N/A')}
- Birth Year: {query.get('birth_year', 'N/A')}
- Birth Place: {query.get('birth_place', 'N/A')}
- Death Year: {query.get('death_year', 'N/A')}
- Death Place: {query.get('death_place', 'N/A')}

Suggest:
1. Alternative spellings of names (common misspellings, variations, nicknames)
2. Possible date ranges to search (accounting for transcription errors)
3. Location variations (nearby towns, old vs new place names)
4. Additional search terms that might help

Format as JSON with keys: name_variations, date_ranges, location_variations, additional_terms"""

    def _build_analysis_prompt(self, query: Dict, results: Dict) -> str:
        results_summary = []
        for source, records in results.items():
            for record in records[:5]:  # Limit to top 5 per source
                results_summary.append(f"Source: {source}, Name: {record.get('name')}, "
                                     f"Birth: {record.get('birth_date')} {record.get('birth_place')}, "
                                     f"Death: {record.get('death_date')} {record.get('death_place')}")

        return f"""Analyze these genealogy search results for the query:
{query}

Results:
{chr(10).join(results_summary[:20])}

Rank the results by likelihood of being the correct person. Consider:
1. Name similarity (accounting for spelling variations)
2. Date accuracy (accounting for estimation errors)
3. Location proximity
4. Consistency across sources

Provide confidence scores (0-1) and recommendations in JSON format."""

    def _parse_enhancement_response(self, response: str, original_query: Dict) -> Dict:
        """Parse AI response to extract enhanced query parameters."""
        # Simple implementation - in production, would parse structured JSON
        return {
            **original_query,
            "ai_enhanced": True,
            "enhancements": {
                "raw_suggestions": response[:500]
            }
        }

    def _parse_analysis_response(self, analysis: str, results: Dict) -> Dict:
        """Parse AI analysis response."""
        return {
            "ranked_results": results,
            "ai_analysis": analysis[:1000],
            "confidence_scores": {}
        }

    def _parse_strategy_response(self, response: str) -> Dict:
        """Parse AI strategy response."""
        return {
            "suggested_sources": ["ancestry", "familysearch", "findmypast", "myheritage"],
            "strategy_notes": response[:500]
        }

    async def _query_openai(self, prompt: str) -> str:
        """Query OpenAI API."""
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a genealogy research assistant. "
                     "Provide structured, helpful responses for family history research."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    async def _query_anthropic(self, prompt: str) -> str:
        """Query Anthropic Claude API."""
        try:
            response = await self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
