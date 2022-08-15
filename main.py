import os
import json
import requests

DEBUG = os.environ.get('DEBUG')

GITHUB_BASE_URL = 'https://api.github.com'
GITHUB_REPOSITORY = os.environ.get('INPUT_GITHUB_REPOSITORY')
GITHUB_TOKEN = os.environ.get("INPUT_GITHUB_TOKEN")

LEETCODE_BASE_URL = "https://leetcode.com"
EMOJI = { "easy": "🟢", "medium": "🟡", "hard": "🔴" }

def get_leetcode_daily_problem():
    body = """
      query questionOfToday {
        activeDailyCodingChallengeQuestion {
          date
          link
          question {
            acRate
            codeDefinition
            content
            difficulty
            dislikes
            enableRunCode
            frontendQuestionId: questionFrontendId
            likes
            metaData
            questionId
            sampleTestCase
            similarQuestions
            status
            stats
            title
            titleSlug
            topicTags {
              name
              id
              slug
            }
          }
        }
      }
    """

    payload = { "query": body, "operationName":"questionOfToday" }

    response = requests.post(url=f"{LEETCODE_BASE_URL}/graphql", json=payload)

    if response.status_code != 200:
        print(f"❌  Leetcode Query Response Status Code: {response.status_code}")
        print(f"    Leetcode Query URL: {LEETCODE_BASE_URL}/graphql")
        return False

    print(f"✅  Leetcode Query Response Status Code: {response.status_code}")
    json_response = response.json()
    return response.json()

def generate_github_issue_body(question) -> str:
    problem_url = f"{LEETCODE_BASE_URL}{question['link']}"

    body = f"# {question['question']['questionId']}. {question['question']['title']}\n"

    body += "\n"
    body += f"[🔗 Problem]({problem_url}) [🧵 Discussion]({problem_url}discuss/) [🙋 Solution]({problem_url}solution/)\n"

    difficulty = question['question']['difficulty'].lower()
    body += "\n"
    body += f"| Difficulty | {EMOJI[difficulty]} |\n"
    body += "| :-- | :-: |\n"
    body += f"| Accept Rate | {question['question']['acRate']:.1f}% |\n"

    body += "\n"
    body += f"🏷️  {process_tags(question['question']['topicTags'])}\n"

    body += f"{question['question']['content']}\n"

    return body

def create_github_issue(title,body):
    if DEBUG: print(f"👉  GITHUB_REPOSITORY: {GITHUB_REPOSITORY}")

    repos_url  = f'{GITHUB_BASE_URL}/repos'
    repo_url   = f'{repos_url}/{GITHUB_REPOSITORY}'
    issues_url = f'{repo_url}/issues'

    session = requests.Session()
    headers = {'Authorization': f'token {GITHUB_TOKEN}',
               'Accept': 'application/vnd.github.v3+json'}

    payload = json.dumps({'title': title, 'body': body})

    if DEBUG:
        print(f"👉  POSTing to {issues_url} with JSON payload:")
        print(payload)

    response = session.post(issues_url, data=payload, headers=headers)
    if response.status_code != 201:
        print(f"❌  Could not create new Github issue!")
        print(f"    Status Code: {response.status_code}")
        print(f"    Response: {response.content}")
        return False

    issue_number = response.json().get("number")
    issue_title  = response.json().get("title")
    print(f"✅  Successfully created Issue #{issue_number}: {issue_title}")
    if DEBUG: print(f"👉  {response.json()}")

    return True

def process_tags(tags) -> str:
    tag_url = f'{LEETCODE_BASE_URL}/tag/'
    return ' '.join(f'#[{t["slug"]}]({tag_url}{t["slug"]}/)' for t in tags)
 
def main():
    leetcode_json_response = get_leetcode_daily_problem()
    question = leetcode_json_response["data"]["activeDailyCodingChallengeQuestion"]

    github_issue_body = generate_github_issue_body(question)
    github_issue_title = f"LC Daily: {question['question']['questionId']}. {question['question']['title']}"

    print(f"ℹ️   github_issue_title: {github_issue_title}")
    if DEBUG: print(f"👉  github_issue_body:\n{github_issue_body}")

    return create_github_issue(github_issue_title,github_issue_body)

if __name__ == "__main__":
    main()
