"""Render public GitHub stats and verified merged upstream PRs using authenticated gh."""
import json
import os
import subprocess
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
LOGIN = os.environ.get('GH_LOGIN', 'Theater-ahyeon')


def api(*args):
    result = subprocess.run(['gh', 'api', *args], capture_output=True, text=True, encoding='utf-8', check=True)
    return json.loads(result.stdout)


def merged_prs():
    query = """query($login:String!, $cursor:String) {
      user(login:$login) { pullRequests(first:100, after:$cursor, states:MERGED,
        orderBy:{field:UPDATED_AT,direction:DESC}) {
        pageInfo { hasNextPage endCursor }
        nodes { number title url mergedAt repository {
          nameWithOwner isPrivate isFork owner { login }
        } }
      } }
    }"""
    prs, cursor = [], None
    while True:
        args = ['graphql', '-f', f'query={query}', '-f', f'login={LOGIN}']
        if cursor:
            args += ['-f', f'cursor={cursor}']
        result = api(*args)
        if result.get('errors') or not result.get('data', {}).get('user'):
            raise RuntimeError('GitHub did not return merged pull requests')
        page = result['data']['user']['pullRequests']
        for pr in page['nodes']:
            repo = pr['repository']
            if pr['mergedAt'] and not repo['isPrivate'] and not repo['isFork'] and repo['owner']['login'].lower() != LOGIN.lower():
                prs.append(pr)
        if not page['pageInfo']['hasNextPage']:
            return sorted(prs, key=lambda pr: pr['mergedAt'], reverse=True)
        next_cursor = page['pageInfo']['endCursor']
        if not next_cursor or next_cursor == cursor:
            raise RuntimeError('Invalid GitHub pagination cursor')
        cursor = next_cursor


def fetch():
    repos = api(f'users/{LOGIN}/repos?per_page=100&type=owner', '--paginate', '--slurp')
    repos = [repo for page in repos for repo in page if not repo['private'] and not repo['fork']]
    query = '''query($login:String!) { user(login:$login) {
      contributionsCollection { contributionCalendar { totalContributions weeks {
        contributionDays { date contributionCount contributionLevel }
      } } }
    } }'''
    result = api('graphql', '-f', f'query={query}', '-f', f'login={LOGIN}')
    if result.get('errors') or not result.get('data', {}).get('user'):
        raise RuntimeError('GitHub did not return a contribution calendar')
    calendar = result['data']['user']['contributionsCollection']['contributionCalendar']
    prs = merged_prs()
    projects = {}
    for pr in prs:
        name = pr['repository']['nameWithOwner']
        projects[name] = projects.get(name, 0) + 1
    return dict(login=LOGIN, generated_at=datetime.now(timezone.utc).isoformat(),
                repositories=len(repos), stars=sum(repo['stargazers_count'] for repo in repos),
                contributions=calendar['totalContributions'], merged_prs=prs, projects=projects)

