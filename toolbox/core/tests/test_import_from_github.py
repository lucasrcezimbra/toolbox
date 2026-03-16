from collections import Counter

from toolbox.core.scripts.import_from_github import build_slug, owner_from_github_url


def test_owner_from_github_url():
    assert owner_from_github_url("https://github.com/httpie/cli") == "httpie"


def test_build_slug_keeps_unique_repo_name():
    name_counts = Counter({"toolbox": 1})

    assert (
        build_slug(
            "toolbox",
            "https://github.com/lucasrcezimbra/toolbox",
            name_counts,
        )
        == "toolbox"
    )


def test_build_slug_prepends_owner_for_duplicate_repo_names():
    name_counts = Counter({"cli": 3})

    assert (
        build_slug("cli", "https://github.com/httpie/cli", name_counts) == "httpie-cli"
    )
    assert build_slug("cli", "https://github.com/cli/cli", name_counts) == "cli-cli"
    assert (
        build_slug("cli", "https://github.com/googleworkspace/cli", name_counts)
        == "googleworkspace-cli"
    )
