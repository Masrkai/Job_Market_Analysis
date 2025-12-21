import json
import html
import os
from bs4 import BeautifulSoup

def parse_description_to_txt(json_input):
    # 1. Parse the JSON string to get the 'description' field
    # (Assuming the input is the full JSON object)
    try:
        data = json.loads(json_input)
        raw_description = data.get("description", "")
    except json.JSONDecodeError:
        # If you passed just the string inside the quotes, use it directly
        raw_description = json_input

    # 2. Convert HTML entities (e.g., &lt; to <)
    unescaped_html = html.unescape(raw_description)

    # 3. Use BeautifulSoup to remove tags and handle line breaks
    soup = BeautifulSoup(unescaped_html, 'html.parser')
    
    # Replace <br> and </li> with actual newlines for readability
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for li in soup.find_all("li"):
        li.insert_before("- ")
        li.append("\n")

    clean_text = soup.get_text()

    # 4. Save to a .txt file
    output_filename = "job_description.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(clean_text.strip())

    print(f"File saved successfully as: {os.path.abspath(output_filename)}")

# Example usage with your provided text
job_json = """
{
    "description": "&lt;strong&gt;About Us&lt;br&gt;&lt;br&gt;&lt;/strong&gt;Notion helps you build beautiful tools..."
}
"""
# Note: I've shortened the 'job_json' variable for the example; 
# you can paste your full string there.

if __name__ == "__main__":
    # You can paste your full "description": "..." block here
    raw_data = {
        "description": "&lt;strong&gt;About Us&lt;br&gt;&lt;br&gt;&lt;/strong&gt;Notion helps you build beautiful tools for your life’s work. In today's world of endless apps and tabs, Notion provides one place for teams to get everything done, seamlessly connecting docs, notes, projects, calendar, and email—with AI built in to find answers and automate work. Millions of users, from individuals to large organizations like Toyota, Figma, and OpenAI, love Notion for its flexibility and choose it because it helps them save time and money.&lt;br&gt;&lt;br&gt;In-person collaboration is essential to Notion's culture. We require all team members to work from our offices on Mondays and Thursdays, our designated Anchor Days. Certain teams or positions may require additional in-office workdays.&lt;br&gt;&lt;br&gt;&lt;strong&gt;About The Role&lt;br&gt;&lt;br&gt;&lt;/strong&gt;As an Early Career Software Engineer at Notion, you’ll help shape core user experiences and accelerate how people discover value in Notion. You'll tackle meaningful challenges with increasing autonomy, crafting code that millions of users will experience. You'll take ownership of projects that matter, make critical technical decisions, and contribute your unique perspective to our product vision. Working alongside passionate experts across design, product, and data, you'll help shape the future of how people work.&lt;br&gt;&lt;br&gt;We’re hiring early career engineers to join us across several teams at Notion. Your recruiter will partner with you to find the team that best aligns with your interests and where you can make the highest impact.&lt;br&gt;&lt;br&gt;What You’ll Achieve&lt;br&gt;&lt;br&gt;&lt;ul&gt;&lt;li&gt;Plan, build, and ship product features from conception to launch, then iterate based on insights and user feedback.&lt;/li&gt;&lt;li&gt;Improve performance, reliability, and quality of key experiences used by millions of users and thousands of organizations.&lt;/li&gt;&lt;li&gt;Run experiments that drive activation, retention, collaboration, and revenue, partnering with design, data science, and research.&lt;/li&gt;&lt;li&gt;Build internal tools and platform improvements that help all engineers ship quickly and safely.&lt;/li&gt;&lt;li&gt;Contribute to team norms, code quality, and a culture of learning and thoughtful tradeoffs.&lt;br&gt;&lt;br&gt;&lt;/li&gt;&lt;/ul&gt;Areas you might work on&lt;br&gt;&lt;br&gt;&lt;ul&gt;&lt;li&gt;Core Notion product features: Help develop, improve, and maintain features for our flagship product, focusing on the editor, databases, sharing, or other key areas that power millions of workflows.&lt;/li&gt;&lt;li&gt;AI and automation: Help develop and integrate intelligent features that make Notion more powerful, contextual, and efficient for our users.&lt;/li&gt;&lt;li&gt;Growth and activation: Work on features that help new users discover Notion's value, improve onboarding experiences, and increase user engagement.&lt;/li&gt;&lt;li&gt;Platform and infrastructure: Contribute to the systems that power Notion's backend services, ensuring reliability, scalability, and performance as our user base grows.&lt;br&gt;&lt;br&gt;&lt;/li&gt;&lt;/ul&gt;Skills You’ll Bring&lt;br&gt;&lt;br&gt;&lt;ul&gt;&lt;li&gt;Proven track record of execution: You have a minimum of 1 year (and up to 3 years) of full-time professional engineering experience, including building world-class product experiences as part of an engineering team. You have solid fundamentals in data structures, algorithms, and distributed systems, with a product-minded, pragmatic approach to solving problems.&lt;/li&gt;&lt;li&gt;Thoughtful problem-solving: You approach problems holistically, starting with a clear and accurate understanding of the context. You think about the implications of what you're building and how it will impact real people's lives. You can navigate ambiguity successfully, decompose complex problems into clean solutions, while also balancing the business impact of what you’re building.&lt;/li&gt;&lt;li&gt;Impact-driven approach to technology: You see technologies as tools to achieve user impact rather than ends in themselves. You care more about building successful systems that solve real problems than about using specific tech stacks or following trends. You stay current with the latest tools like Cursor, Claude Code, and other AI-assisted development environments, you're pragmatic about choosing the right tool for the job, focusing on what delivers the most value to users and the business.&lt;/li&gt;&lt;li&gt;Proactive communication and high agency: You own your work, communicating clearly about progress and blockers. You don't wait for instructions for every step but rather show initiative in identifying what needs to be done and driving projects forward. You ask questions when needed while independently finding solutions to problems.&lt;br&gt;&lt;br&gt;&lt;/li&gt;&lt;/ul&gt;Nice to Have&lt;br&gt;&lt;br&gt;&lt;ul&gt;&lt;li&gt;Experience with parts of our stack like React, TypeScript, Node.js, Postgres, or with experimentation and analytics tooling.&lt;/li&gt;&lt;li&gt;Exposure to distributed systems, observability, CI/CD, or infrastructure fundamentals.&lt;/li&gt;&lt;li&gt;An interest in product quality and craft, and in helping others stay in flow.&lt;/li&gt;&lt;li&gt;You've heard of computing pioneers like Ada Lovelace, Douglas Engelbart, Alan Kay, and others—and understand why we're big fans of their work.&lt;br&gt;&lt;br&gt;&lt;/li&gt;&lt;/ul&gt;We hire talented and passionate people from a variety of backgrounds because we want our global employee base to represent the wide diversity of our customers. If you’re excited about a role but your past experience doesn’t align perfectly with every bullet point listed in the job description, we still encourage you to apply. If you’re a builder at heart, share our company values, and enthusiastic about making software toolmaking ubiquitous, we want to hear from you.&lt;br&gt;&lt;br&gt;Notion is proud to be an equal opportunity employer. We do not discriminate in hiring or any employment decision based on race, color, religion, national origin, age, sex (including pregnancy, childbirth, or related medical conditions), marital status, ancestry, physical or mental disability, genetic information, veteran status, gender identity or expression, sexual orientation, or other applicable legally protected characteristic. Notion considers qualified applicants with criminal histories, consistent with applicable federal, state and local law. Notion is also committed to providing reasonable accommodations for qualified individuals with disabilities and disabled veterans in our job application procedures. If you need assistance or an accommodation due to a disability, please let your recruiter know.&lt;br&gt;&lt;br&gt;Notion is committed to providing highly competitive cash compensation, equity, and benefits. The compensation offered for this role will be based on multiple factors such as location, the role’s scope and complexity, and the candidate’s experience and expertise, and may vary from the range provided below. For roles based in San Francisco or New York City, the estimated base salary range for this role is $126,000 - $180,000 per year.&lt;br&gt;&lt;br&gt;By clicking “Submit Application”, I understand and agree that Notion and its affiliates and subsidiaries will collect and process my information in accordance with Notion’s Global Recruiting Privacy Policy and NYLL 144.&lt;br&gt;&lt;br&gt;"
    }
    parse_description_to_txt(json.dumps(raw_data))