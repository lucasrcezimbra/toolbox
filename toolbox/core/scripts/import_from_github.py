import sqlite3

from django.db.utils import IntegrityError

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


def run():
    conn = sqlite3.connect("./github.sqlite3")
    cursor = conn.execute(SQL)
    rows = cursor.fetchall()

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
        t = Tool(
            archived=archived,
            added_at=starred_at,
            name=name,
            url_docs=homepage if is_url_docs(homepage) else "",
            url_github=url_github.lower(),
            slug=name,
            stargazers=stargazers_count,
            forks=forks_count,
            last_commit_date=pushed_at,
        )
        try:
            t.save()
        except IntegrityError:
            # TODO; improve this; it will not work when the user has more than 2
            #       tools with the same name
            t.slug = f"{name}2"
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
