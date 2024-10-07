import sqlite3

from toolbox.core.models import Tool

SQL = """
SELECT
    starred_at,
    repos.html_url,
    repos.name,
    repos.language
FROM
    stars
    JOIN repos ON
        stars.repo = repos.id
ORDER BY
    starred_at
"""


def run():
    conn = sqlite3.connect("./github.sqlite3")
    cursor = conn.execute(SQL)
    rows = cursor.fetchall()

    for starred_at, html_url, name, language in rows:
        t = Tool(added_at=starred_at, url_github=html_url, name=name)
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
