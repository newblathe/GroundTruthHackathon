# ------------------------------------------------------------
# insights.py
# This module communicates with the Groq Llama 3.1 model to generate human-like narrative insights from dataset summary statistics.
#
# The insights engine uses a structured prompt to replicate
# a senior analyst's reasoning style, producing:
#   1. Trends
#   2. Patterns
#   3. Anomalies
#   4. Risks
#   5. Recommendations
# ------------------------------------------------------------

from groq import Groq

client = Groq(api_key="Placholder API")

# AI Insights Generator
def generate_insights(summary):
    prompt = f"""
    You are a senior data analyst. Write a highly professional insight
    report based on the summary below.

    Summary:
    {summary}

    Include:
    - Key trends
    - Interesting patterns
    - Anomalies
    - Risks
    - Executive recommendations
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
