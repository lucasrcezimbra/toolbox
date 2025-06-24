import re
import sqlite3
from datetime import datetime

import requests
from django.db.utils import IntegrityError
from django.utils import timezone

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
    repos.forks_count
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
    ) in rows:
        # Get the last commit date from GitHub API
        owner, repo = extract_owner_repo(url_github)
        last_commit_at = None
        if owner and repo:
            last_commit_at = get_latest_commit_date(owner, repo)
            if last_commit_at:
                print(f"Found last commit date for {name}: {last_commit_at}")
            else:
                print(f"Could not fetch last commit date for {name}")
        else:
            print(f"Could not parse GitHub URL for {name}: {url_github}")

        t = Tool(
            archived=archived,
            added_at=starred_at,
            name=name,
            url_docs=homepage if is_url_docs(homepage) else "",
            url_github=url_github.lower(),
            slug=name,
            stargazers=stargazers_count,
            forks=forks_count,
            last_commit_at=last_commit_at,
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


def extract_owner_repo(url):
    match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if match:
        return match.group(1), match.group(2)
    return None, None


def get_latest_commit_date(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"

    try:
        response = requests.get(url, params={"per_page": 1})
        response.raise_for_status()

        commits = response.json()
        if commits and len(commits) > 0:
            commit_date_str = commits[0]["commit"]["committer"]["date"]
            return datetime.strptime(commit_date_str, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc
            )
    except Exception as e:
        print(f"Error fetching commit data for {owner}/{repo}: {str(e)}")

    return None
