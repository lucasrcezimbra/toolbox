import re
from datetime import datetime

import requests
from django.utils import timezone

from toolbox.core.models import Tool


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


def run():
    tools = Tool.objects.all()
    updated_count = 0

    for tool in tools:
        owner, repo = extract_owner_repo(tool.url_github)
        if owner and repo:
            last_commit_date = get_latest_commit_date(owner, repo)
            if last_commit_date:
                tool.last_commit_at = last_commit_date
                tool.save(update_fields=["last_commit_at"])
                updated_count += 1
                print(f"Updated {tool.name} with last commit date: {last_commit_date}")
            else:
                print(f"Could not fetch last commit date for {tool.name}")
        else:
            print(f"Could not parse GitHub URL for {tool.name}: {tool.url_github}")

    print(f"Updated {updated_count} out of {len(tools)} tools with last commit dates.")
