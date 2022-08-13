import os
import json
import requests  # noqa We are just importing this to prove the dependency installed correctly


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
            isFavor
            paidOnly: isPaidOnly
            status
            title
            titleSlug
            hasVideoSolution
            hasSolution
            topicTags {
              name
              id
              slug
            }
          }
        }
      }
    """

    payload = {
      "query": body,
      "operationName":"questionOfToday" }

    response = requests.post(url=url, json=payload)
    print("response status code: ", response.status_code)
    if response.status_code == 200:
        print("response: ", json.dumps(response.json(), indent=3))

if __name__ == "__main__":
    main()
