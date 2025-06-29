from django.shortcuts import render
import json
import os
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import anthropic

load_dotenv()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{{ name }} - {{ label }}</title>
  <link rel="stylesheet" href="./styles.css" />
</head>
<body>
  <header>
    <h1>{{ name }}</h1>
    <h3>{{ label }}</h3>
    <p>
      <a href="mailto:{{ email }}">{{ email }}</a> ·
      <a href="tel:{{ phone }}">{{ phone }}</a> ·
      <a href="{{ website }}" target="_blank">{{ website }}</a>
    </p>
    <p>
      {{#each profiles}}
        <a href="{{ url }}" target="_blank">{{ network }}</a>{{#unless @last}} | {{/unless}}
      {{/each}}
    </p>
  </header>

  <section>
    <h2>About</h2>
    <p>{{ summary }}</p>
    <p><strong>Location:</strong> {{ location.address }}, {{ location.city }}, {{ location.region }} {{ location.postalCode }}, {{ location.country }}</p>
  </section>

  <section>
    <h2>Work Experience</h2>
    {{#each work}}
      <div>
        <h3>{{ position }} · {{ company }} <small>({{ startDate }}–{{ endDate }})</small></h3>
        <p>{{ summary }}</p>
        <ul>
          {{#each highlights}}
            <li>{{ this }}</li>
          {{/each}}
        </ul>
      </div>
    {{/each}}
  </section>

  <section>
    <h2>Projects</h2>
    {{#each projects}}
      <p><strong><a href="{{ url }}" target="_blank">{{ name }}</a></strong><br>{{ description }}</p>
      <div>
        {{#each keywords}}
          <span class="highlight">{{ this }}</span>
        {{/each}}
      </div>
    {{/each}}
  </section>

  <section>
    <h2>Skills</h2>
    <div class="two-col">
      {{#each skills}}
        <div>
          <h4>{{ name }} ({{ level }})</h4>
          <div>
            {{#each keywords}}
              <span class="highlight">{{ this }}</span>
            {{/each}}
          </div>
        </div>
      {{/each}}
    </div>
  </section>

  <section>
    <h2>Education</h2>
    {{#each education}}
      <p><strong>{{ institution }}</strong><br>
        {{ studyType }} in {{ area }} ({{ startDate }}–{{ endDate }}), GPA: {{ gpa }}</p>
      <ul>
        {{#each courses}}
          <li>{{ this }}</li>
        {{/each}}
      </ul>
    {{/each}}
  </section>

  <section>
    <h2>Languages</h2>
    <ul>
      {{#each languages}}
        <li>{{ language }} – {{ fluency }}</li>
      {{/each}}
    </ul>
  </section>

  <section>
    <h2>Interests</h2>
    <div>
      {{#each interests}}
        <span class="highlight">{{ name }}</span>
      {{/each}}
    </div>
  </section>

  <footer>
    &copy; {{ year }} {{ name }} · Built with ❤️ and HTML/CSS
  </footer>
</body>
</html>
"""

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


@csrf_exempt
def render_resume(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST method allowed.")

    try:
        data = json.loads(request.body)
        resume = data["resume"]
    except (json.JSONDecodeError, KeyError):
        return HttpResponseBadRequest("Invalid JSON or missing 'resume' key.")

    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=2000,
        temperature=1,
        system=(
            "You create HTML versions of resumes. You will write only in HTML without CSS, and nothing more. "
            "You will link to /styles.css for the CSS. Your response will not be contained within a codeblock. "
            "The code will be one line of HTML, no newlines. You will modify the About section based on the contents of the resume. "
            f"You will use this template for the HTML: {HTML_TEMPLATE}"
        ),
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Please make me a single-page HTML version of this resume: {resume}"
                    }
                ]
            }
        ]
    )

    return JsonResponse({"html": message.content[0].text})
