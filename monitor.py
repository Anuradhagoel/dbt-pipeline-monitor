import json
import os
from groq import Groq


def parse_dbt_results(path="target/run_results.json"):
    """
    Reads dbt's run_results.json and extracts failed and passed tests.
    dbt saves this file every time you run `dbt test`.
    """
    with open(path) as f:
        results = json.load(f)

    failures = []
    passes = []

    for result in results["results"]:
        # unique_id looks like: test.pipeline_monitor.not_null_orders_summary_amount.xxx
        # We split by "." and take the last part as a readable name
        node_name = result["unique_id"].split(".")[-1]
        status = result["status"]

        if status == "fail":
            failures.append({
                "test": node_name,
                "status": status,
                "failures": result.get("failures", 0)
            })
        elif status == "pass":
            passes.append(node_name)

    return failures, passes


def get_ai_summary(failures):
    """
    Sends the failure info to Groq (free AI API) and gets back
    a plain English explanation of what broke and what to check.
    """
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    # Build a readable list of failures to send to the AI
    failure_text = "\n".join([
        f"- Test '{f['test']}' failed with {f['failures']} bad rows"
        for f in failures
    ])

    prompt = f"""
    You are a data quality assistant. These dbt tests just failed:

    {failure_text}

    Write a short, clear alert message (under 100 words) for a data team explaining:
    1. What failed
    2. What data might be affected
    3. What to check first

    Use plain English. No technical jargon.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def main():
    print("Running dbt Pipeline Monitor...")
    print("=" * 50)

    failures, passes = parse_dbt_results()

    print(f"\n✅ Passed: {len(passes)} tests")
    print(f"❌ Failed: {len(failures)} tests")

    if failures:
        print("\nFailed tests:")
        for f in failures:
            print(f"  - {f['test']} ({f['failures']} bad rows)")

        print("\nGenerating AI summary...")
        summary = get_ai_summary(failures)

        print("\n" + "=" * 50)
        print("AI ALERT SUMMARY:")
        print("=" * 50)
        print(summary)
    else:
        print("\nAll tests passed! Pipeline is healthy. ✅")


if __name__ == "__main__":
    main()
