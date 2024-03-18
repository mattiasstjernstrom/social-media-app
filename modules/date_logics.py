from datetime import datetime, timedelta


def humanize_time(dt):
    # !Deprecated, fix
    now = datetime.utcnow()
    diff = now - dt

    if diff < timedelta(seconds=10):
        return "Now"
    elif diff < timedelta(minutes=1):
        return "A moment ago"
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() / 60)
        if minutes == 1:
            return "One minute ago"
        else:
            return f"{minutes} minutes ago"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        if hours == 1:
            return "One hour ago"
        else:
            return f"{hours} hours ago"
    elif diff < timedelta(days=2):
        return "Igår"
    elif diff < timedelta(days=365):
        return dt.strftime("%B %d")
    else:
        return dt.strftime("%Y-%m-%d")
