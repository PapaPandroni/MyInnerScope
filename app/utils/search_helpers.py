import re
from typing import Union, List
from datetime import datetime, date
from flask import render_template, redirect
from werkzeug.wrappers import Response as WerkzeugResponse
from markupsafe import escape
from ..models import DiaryEntry


def handle_search(
    user_id: int, 
    display_name: str, 
    diary_dates: List[date], 
    search_text: str, 
    search_date: str,
    rating: int = None
) -> Union[str, WerkzeugResponse]:
    """Handle search functionality for diary entries.
    
    Args:
        user_id: The ID of the user performing the search.
        display_name: The user's display name.
        diary_dates: List of dates with diary entries.
        search_text: The text to search for.
        search_date: The date to filter by.
        rating: Optional rating filter (-1 or 1).
        
    Returns:
        Rendered template or redirect response.
    """
    # If only date is provided (no search text), redirect to that date
    if search_date and not search_text:
        return redirect(f"/read-diary?date={search_date}")

    # Build the search query
    query = DiaryEntry.query.filter_by(user_id=user_id)

    # Add date filter if specified
    if search_date:
        try:
            target_date = datetime.strptime(search_date, "%Y-%m-%d").date()
            query = query.filter(DiaryEntry.entry_date == target_date)
        except ValueError:
            # Invalid date, ignore the date filter
            pass

    # Add text search if specified
    if search_text:
        query = query.filter(DiaryEntry.content.ilike(f"%{search_text}%"))

    # Add rating filter if specified
    if rating is not None:
        query = query.filter(DiaryEntry.rating == rating)

    # Execute the search
    search_results = query.order_by(DiaryEntry.entry_date.desc()).all()

    # Create search result snippets with highlighting
    result_data = []
    for entry in search_results:
        snippet = create_search_snippet(entry.content, search_text)
        formatted_date = entry.entry_date.strftime("%A, %B %d, %Y")

        result_data.append(
            {
                "date": entry.entry_date,
                "formatted_date": formatted_date,
                "snippet": snippet,
            }
        )

    return render_template(
        "reader/read_diary.html",
        display_name=display_name,
        diary_dates=diary_dates,
        search_results=result_data,
        show_search_results=True,
    )


def create_search_snippet(content: str, search_text: str, context_chars: int = 20) -> str:
    """Create a search snippet with highlighted search terms.
    
    Args:
        content: The full content to create a snippet from.
        search_text: The text to highlight in the snippet.
        context_chars: Number of characters to show around the match.
        
    Returns:
        HTML snippet with highlighted search terms.
    """
    if not search_text:
        return content[:80] + "..." if len(content) > 80 else content

    # Find the search text (case insensitive)
    content_lower = content.lower()
    search_lower = search_text.lower()

    match_index = content_lower.find(search_lower)
    if match_index == -1:
        return content[:80] + "..." if len(content) > 80 else content

    # Calculate snippet boundaries
    start = max(0, match_index - context_chars)
    end = min(len(content), match_index + len(search_text) + context_chars)

    # Extract snippet
    snippet = content[start:end]

    # Add ellipsis if we're not at the beginning/end
    if start > 0:
        snippet = "..." + snippet
    if end < len(content):
        snippet = snippet + "..."

    # Highlight the search term (case insensitive replacement)
    snippet = re.sub(
        re.escape(search_text),
        f"<mark>{escape(search_text)}</mark>",
        snippet,
        flags=re.IGNORECASE,
    )

    return snippet
