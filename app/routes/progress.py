from typing import Union
from flask import Blueprint, render_template, redirect, session, send_file, request, Response
from werkzeug.wrappers import Response as WerkzeugResponse
from datetime import date, datetime, timezone
from ..models import User, DiaryEntry, DailyStats, db

from ..utils.progress_helpers import (
    get_display_name,
    get_today_stats,
    get_total_points,
    get_current_streak,
    get_longest_streak,
    get_total_entries,
    get_points_data,
    get_top_days_with_entries,
    get_weekday_data,
    get_sample_weekday_data,
    get_trend_message,
    get_recent_entries,
    get_unique_weekdays_with_entries,
)
from ..utils.goal_helpers import (
    get_current_goals,
    get_goal_statistics,
    get_goal_history,
)

progress_bp = Blueprint("progress", __name__)


@progress_bp.route("/progress")
def progress() -> Union[str, WerkzeugResponse]:
    if "user_id" not in session:
        return redirect("/login")
    user_id = session["user_id"]
    user = User.query.get(user_id)
    today = datetime.now(timezone.utc).date()

    display_name = get_display_name(user)
    points_today = get_today_stats(user_id, today)
    total_points = get_total_points(user_id)
    current_streak = get_current_streak(user_id)
    longest_streak = get_longest_streak(user_id)
    total_entries = get_total_entries(user_id)
    points_data = get_points_data(user_id)
    top_days_with_entries = get_top_days_with_entries(user_id)
    weekday_data, has_sufficient_weekday_data = get_weekday_data(user_id)
    sample_weekday_data = get_sample_weekday_data()
    trend_message = get_trend_message(user_id, today)

    # Get all current goals
    current_goals = get_current_goals(user_id)

    # Get goal statistics
    goal_stats = get_goal_statistics(user_id)

    # Word Cloud logic
    entries = DiaryEntry.query.filter_by(user_id=user_id).all()
    entry_count = len(entries)
    has_sufficient_wordcloud_data = entry_count >= 10
    wordcloud_data = []
    if has_sufficient_wordcloud_data:
        import re
        from collections import Counter

        # most common stop words in English
        stop_words = set(
            [
                "the",
                "and",
                "is",
                "in",
                "it",
                "of",
                "to",
                "a",
                "for",
                "on",
                "with",
                "as",
                "at",
                "by",
                "an",
                "be",
                "this",
                "that",
                "from",
                "or",
                "are",
                "was",
                "but",
                "not",
                "have",
                "has",
                "had",
                "they",
                "you",
                "i",
                "we",
                "he",
                "she",
                "his",
                "her",
                "their",
                "our",
                "my",
                "your",
                "so",
                "if",
                "do",
                "did",
                "does",
                "can",
                "will",
                "just",
                "about",
                "me",
                "what",
                "when",
                "which",
                "who",
                "how",
                "all",
                "no",
                "out",
                "up",
                "down",
                "into",
                "more",
                "than",
                "then",
                "them",
                "were",
                "been",
                "would",
                "could",
                "should",
                "also",
                "because",
                "too",
                "very",
                "get",
                "got",
                "go",
                "going",
                "one",
                "now",
                "over",
                "after",
                "before",
                "off",
                "even",
                "still",
                "only",
                "see",
                "such",
                "where",
                "why",
                "these",
                "those",
                "each",
                "other",
                "some",
                "any",
                "every",
                "much",
                "many",
                "most",
                "few",
                "lot",
                "lots",
                "may",
                "might",
                "must",
                "like",
                "want",
                "needs",
                "need",
                "make",
                "made",
                "back",
                "again",
                "new",
                "old",
                "first",
                "last",
                "time",
                "day",
                "days",
                "week",
                "weeks",
                "month",
                "months",
                "year",
                "years",
                "today",
                "tomorrow",
                "yesterday",
                "now",
                "soon",
                "late",
                "early",
                "never",
                "always",
                "sometimes",
                "often",
                "usually",
                "once",
                "twice",
                "next",
                "previous",
                "another",
                "same",
                "different",
                "right",
                "left",
                "here",
                "there",
                "home",
                "work",
                "school",
                "place",
                "thing",
                "things",
                "way",
                "ways",
                "life",
                "lives",
                "person",
                "people",
                "man",
                "woman",
                "child",
                "children",
                "friend",
                "friends",
                "family",
                "families",
                "parent",
                "parents",
                "mother",
                "father",
                "mom",
                "dad",
                "sister",
                "brother",
                "son",
                "daughter",
                "husband",
                "wife",
                "partner",
                "boyfriend",
                "girlfriend",
                "teacher",
                "student",
                "class",
                "classes",
                "group",
                "groups",
                "team",
                "teams",
                "member",
                "members",
                "leader",
                "lead",
                "follow",
                "following",
                "followed",
                "find",
                "found",
                "lose",
                "lost",
                "give",
                "gave",
                "take",
                "took",
                "keep",
                "kept",
                "let",
                "lets",
                "put",
                "set",
                "run",
                "ran",
                "walk",
                "walked",
                "move",
                "moved",
                "stop",
                "stopped",
                "start",
                "started",
                "end",
                "ended",
                "begin",
                "began",
                "finish",
                "finished",
                "try",
                "tried",
                "use",
                "used",
                "work",
                "worked",
                "play",
                "played",
            ]
        )

        all_text = " ".join(entry.content for entry in entries)
        words = re.findall(r"\b\w+\b", all_text.lower())
        filtered = [w for w in words if w not in stop_words and len(w) > 2]
        freq = Counter(filtered)

        # Get the most common words
        most_common = freq.most_common(50)  # Get more words initially

        if most_common:
            # Normalize frequencies to a 0-100 scale
            max_freq = most_common[0][1]  # Highest frequency
            min_freq = (
                most_common[-1][1] if len(most_common) > 1 else 1
            )  # Lowest frequency

            # Create normalized word cloud data
            wordcloud_data = []
            for word, count in most_common[:30]:  # Take top 30
                # Normalize to 10-100 scale (avoid too small values)
                if max_freq == min_freq:
                    normalized_weight = 50  # If all words have same frequency
                else:
                    # Scale from 70 to 150
                    normalized_weight = 70 + (
                        150 * (count - min_freq) / (max_freq - min_freq)
                    )

                wordcloud_data.append([word, int(normalized_weight)])
        else:
            wordcloud_data = []

    # Count positive and improvement entries
    num_change = sum(1 for e in entries if e.rating == -1)
    num_positive = sum(1 for e in entries if e.rating == 1)

    # Check if user should see onboarding tour (new user with no entries)
    recent_entries = get_recent_entries(user_id)
    is_new_user = len(recent_entries) == 0
    
    # Get unique weekdays count for progress display
    unique_weekdays_count = get_unique_weekdays_with_entries(user_id)

    return render_template(
        "progress/progress.html",
        points_today=points_today,
        total_points=total_points,
        current_streak=current_streak,
        longest_streak=longest_streak,
        total_entries=total_entries,
        points_data=points_data,
        top_days=top_days_with_entries,
        weekday_data=weekday_data,
        has_sufficient_weekday_data=has_sufficient_weekday_data,
        sample_weekday_data=sample_weekday_data,
        trend_message=trend_message,
        display_name=display_name,
        current_goals=current_goals,
        goal_stats=goal_stats,
        has_sufficient_wordcloud_data=has_sufficient_wordcloud_data,
        wordcloud_data=wordcloud_data,
        wordcloud_entry_count=entry_count,
        num_change=num_change,
        num_positive=num_positive,
        is_new_user=is_new_user,
        unique_weekdays_count=unique_weekdays_count,
    )
