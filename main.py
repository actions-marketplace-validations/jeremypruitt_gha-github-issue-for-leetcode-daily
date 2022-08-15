import os
import json
import requests

AUTH_TOKEN = os.environ.get('GITHUB_TOKEN')
DEBUG = os.environ.get('DEBUG')
GITHUB_BASE_URL = 'https://api.github.com'
LEETCODE_BASE_URL = "https://www.leetcode.com"
EMOJI = { "easy": "🟢", "medium": "🟡", "hard": "🔴" }

# ---------------------------------------------------------------------
# Create Github Issue
# ---------------------------------------------------------------------
def create_github_issue(title,body):
    repo_name  = os.environ.get('GITHUB_REPOSITORY')
    if DEBUG: print(f'repo_name: {repo_name}')

    repos_url  = f'{GITHUB_BASE_URL}/repos'
    repo_url   = f'{repos_url}/{repo_name}'
    issues_url = f'{repo_url}/issues'

    session = requests.Session()
    headers = {'Authorization': f'token {AUTH_TOKEN}',
               'Accept': 'application/vnd.github.v3+json'}

    payload = json.dumps({'title': title, 'body': body})

    if DEBUG:
        print(f'POSTing to {issues_url} with JSON payload:')
        print(payload)

    response = session.post(issues_url, data=payload, headers=headers)
    if response.status_code != 201:
        print(f'Could not create new Github:')
        print(f'    Status Code: {response.status_code}')
        print(f'    Response: {response.content}')

    issue_number = response.json().get("number")
    issue_title  = response.json().get("title")
    print('Successfully created Issue #{issue_number}: {issue_title}')
    if DEBUG: print(response.json())

def process_tags(tags) -> str:
    tag_url = f'{LEETCODE_BASE_URL}/tag/'
    return ' '.join(f'#[{t["slug"]}]({tag_url}{t["slug"]}/)' for t in tags)
 
def main():
    url = "https://leetcode.com/graphql"
    body = """
      query questionOfToday {
        activeDailyCodingChallengeQuestion {
          date
          userStatus
          link
          question {
            acRate
            difficulty
            freqBar
            frontendQuestionId: questionFrontendId
            hasSolution
            hasVideoSolution
            isFavor
            paidOnly: isPaidOnly
            status
            title
            titleSlug
            codeDefinition
            codeSnippets {
                lang
                langSlug
                code
                __typename
            }
            content
            dislikes
            enableRunCode
            exampleTestcases
            hints
            likes
            metaData
            questionId
            sampleTestCase
            similarQuestions
            stats
            topicTags {
              name
              id
              slug
              translatedName
              __typename
            }
            translatedContent
            translatedTitle
          }
        }
      }
    """

    payload = {
      "query": body,
      "operationName":"questionOfToday" }

    response = requests.post(url=url, json=payload)
    print(f'response status code: {response.status_code}')
    if response.status_code == 200:
        json_response = response.json()
        pretty_json_response = json.dumps(json_response, indent=3)

        data = json_response["data"]
        question = data["activeDailyCodingChallengeQuestion"]

        problem_url = f"{LEETCODE_BASE_URL}{question['link']}"

        new_response = f"# {question['question']['questionId']}. {question['question']['title']}\n"

        new_response += "\n"
        new_response += f"[🔗 Problem]({problem_url}) [🧵 Discussion]({problem_url}discuss/) [🙋 Solution]({problem_url}solution/)\n"

        difficulty = question['question']['difficulty'].lower()
        new_response += "\n"
        new_response += f"| Difficulty | {EMOJI[difficulty]} |\n"
        new_response += "| :-- | :-: |\n"
        new_response += f"| Accept Rate | {question['question']['acRate']:.1f}% |\n"

        new_response += "\n"
        new_response += f"🏷️  {process_tags(question['question']['topicTags'])}\n"

        new_response += f"{question['question']['content']}\n"

        if DEBUG:
            new_response += "\n"
            new_response += "## Raw JSON Payload\n"
            new_response += "<details>\n"
            new_response += "    <summary>Click to expand...</summary>\n\n"
            new_response += "```json\n"
            new_response += f"{pretty_json_response}\n"
            new_response += "```\n\n"
            new_response += "</details>\n"

        print(f'response: {new_response}')
        create_github_issue(f"TEST - LC Daily: {question['question']['questionId']}. {question['question']['title']}",new_response)



    # ---------------------------------------------------------------------

if __name__ == "__main__":
    main()
