import sqlite3
from collections import Counter
from urllib.parse import urlparse

from toolbox.core.models import Tool

SQL = """
SELECT
    starred_at,
    repos.html_url,
    repos.name,
    repos.language,
    repos.homepage,
    repos.archived,
    repos.stargazers_count,
    repos.forks_count,
    repos.pushed_at
FROM
    stars
    JOIN repos ON
        stars.repo = repos.id
ORDER BY
    starred_at
"""


def is_url_docs(url):
    if not url:
        return False
    elif "readthedocs" in url:
        return True
    elif "rtfd" in url:
        return True
    elif "//docs." in url:
        return True
    else:
        return False


def owner_from_github_url(url):
    return urlparse(url).path.strip("/").split("/", maxsplit=1)[0]


def build_slug(name, url_github, name_counts):
    if name_counts[name] == 1:
        return name
    return f"{owner_from_github_url(url_github)}-{name}"


def run():
    conn = sqlite3.connect("./github.sqlite3")
    cursor = conn.execute(SQL)
    rows = cursor.fetchall()
    name_counts = Counter(name for _, _, name, *_ in rows)

    for (
        starred_at,
        url_github,
        name,
        language,
        homepage,
        archived,
        stargazers_count,
        forks_count,
        pushed_at,
    ) in rows:
        normalized_url_github = url_github.lower()
        t = Tool(
            archived=archived,
            added_at=starred_at,
            name=name,
            url_docs=homepage if is_url_docs(homepage) else "",
            url_github=normalized_url_github,
            slug=build_slug(name, normalized_url_github, name_counts),
            stargazers=stargazers_count,
            forks=forks_count,
            last_commit_date=pushed_at,
        )
        t.save()

        tags = ["opensource"]
        if language:
            tags.append(tagify(language))
        t.tags.add(*tags)


def tagify(s):
    s = s.lower()
    s = s.replace("#", "-sharp")
    s = s.replace("++", "pp")
    return s
