from datetime import datetime, timedelta


from datetime import datetime, timedelta


def humanize_time(dt):
    now = datetime.utcnow()
    diff = now - dt

    if diff < timedelta(minutes=1):
        return "a moment ago"
    elif diff < timedelta(hours=1):
        return f"{int(diff.total_seconds() / 60)} minutes ago"
    elif diff < timedelta(hours=2):
        return "one hour ago"
    elif diff < timedelta(days=1):
        return f"{int(diff.total_seconds() / 3600)} hours ago"
    elif diff < timedelta(days=2):
        return "yesterday"
    elif diff < timedelta(days=365):
        return dt.strftime("%B %d")
    else:
        return dt.strftime("%Y-%m-%d")
