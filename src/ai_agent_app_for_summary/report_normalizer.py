from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _normalize_string(value: Any) -> str | None:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped if stripped else None
    return None


def _normalize_topic(topic: Any) -> dict[str, Any]:
    topic = topic if isinstance(topic, dict) else {}

    key_takeaways = topic.get("key_takeaways")
    if isinstance(key_takeaways, list):
        normalized_takeaways = [
            _normalize_string(item) for item in key_takeaways[:3]
        ]
        while len(normalized_takeaways) < 3:
            normalized_takeaways.append(None)
    else:
        normalized_takeaways = [None, None, None]

    related_links = topic.get("related_links")
    normalized_links: list[dict[str, Any]] = []
    if isinstance(related_links, list):
        for link in related_links:
            link = link if isinstance(link, dict) else {}
            normalized_links.append(
                {
                    "label": _normalize_string(link.get("label")),
                    "url": _normalize_string(link.get("url")),
                }
            )

    youtube_videos = topic.get("youtube_videos")
    normalized_videos: list[dict[str, Any]] = []
    if isinstance(youtube_videos, list):
        for video in youtube_videos[:2]:
            video = video if isinstance(video, dict) else {}
            normalized_videos.append(
                {
                    "title": _normalize_string(video.get("title")),
                    "url": _normalize_string(video.get("url")),
                    "channel_name": _normalize_string(video.get("channel_name")),
                    "publish_date": _normalize_string(video.get("publish_date")),
                    "description": _normalize_string(video.get("description")),
                }
            )
    while len(normalized_videos) < 2:
        normalized_videos.append(
            {
                "title": None,
                "url": None,
                "channel_name": None,
                "publish_date": None,
                "description": None,
            }
        )

    if not normalized_links:
        normalized_links = [{"label": None, "url": None}]

    return {
        "topic_title": _normalize_string(topic.get("topic_title")),
        "category": _normalize_string(topic.get("category")),
        "source": _normalize_string(topic.get("source")),
        "publish_date": _normalize_string(topic.get("publish_date")),
        "article_url": _normalize_string(topic.get("article_url")),
        "plain_summary": _normalize_string(topic.get("plain_summary")),
        "key_takeaways": normalized_takeaways,
        "related_links": normalized_links,
        "youtube_videos": normalized_videos,
    }


def normalize_report_payload(payload: Any) -> dict[str, Any]:
    payload = payload if isinstance(payload, dict) else {}

    topics_input = payload.get("topics")
    topics: list[dict[str, Any]] = []
    if isinstance(topics_input, list):
        topics = [_normalize_topic(topic) for topic in topics_input[:7]]

    while len(topics) < 7:
        topics.append(_normalize_topic({}))

    total_topics = payload.get("total_topics")
    if isinstance(total_topics, int):
        normalized_total_topics = total_topics
    else:
        normalized_total_topics = len(topics)

    return {
        "generated_at": _normalize_string(payload.get("generated_at")),
        "report_title": _normalize_string(payload.get("report_title")),
        "total_topics": normalized_total_topics,
        "date_range": _normalize_string(payload.get("date_range")),
        "topics": topics,
    }


def normalize_report_file(report_path: Path) -> dict[str, Any]:
    try:
        raw_text = report_path.read_text(encoding="utf-8")
        parsed = json.loads(raw_text)
    except Exception:
        parsed = {}

    normalized = normalize_report_payload(parsed)
    report_path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
    return normalized
