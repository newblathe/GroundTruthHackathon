from groq import Groq

client = Groq(api_key="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")

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
