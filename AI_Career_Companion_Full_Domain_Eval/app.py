from flask import Flask, render_template, request
import os
import PyPDF2
import spacy

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

career_domains = {
    "AI/ML": {
        "keywords": ["machine learning", "tensorflow", "pytorch", "keras", "neural networks", "deep learning", "nlp", "cv", "python", "data analysis"],
        "company": "Google, Microsoft, Nvidia, Tesla, IBM",
        "role": "Machine Learning Engineer",
        "learning": "Coursera ML by Andrew Ng, Kaggle Competitions, DeepLearning.ai",
        "job_links": [
            "https://www.linkedin.com/jobs/machine-learning-engineer-jobs",
            "https://www.indeed.com/q-Machine-Learning-Engineer-jobs.html"
        ],
        "roadmap": {
            "steps": ["Learn Python & Statistics", "Understand Machine Learning Algorithms", "Deep Dive into Deep Learning", "Explore NLP and Computer Vision", "Work on Real-World Projects"],
            "tools": ["TensorFlow, PyTorch, Keras, scikit-learn, Pandas, Jupyter Notebooks"],
            "certifications": ["DeepLearning.ai Coursera, Google AI ML Certificate"],
            "roles_salary": ["Junior ML Engineer ($75k)", "ML Engineer ($110k)", "Senior ML Engineer ($150k)"]
        }
    },
    "Data Science": {
        "keywords": ["r", "python", "sql", "spss", "sas", "matlab", "eviews", "hadoop", "hive", "mrjob", "spark", "storm",
                     "tableau", "d3.js", "gephi", "git", "aws", "bash", "neo4j", "qg"],
        "company": "Google, IBM, Infosys, Accenture",
        "role": "Data Scientist",
        "learning": "Coursera ML by Andrew Ng, Kaggle competitions",
        "job_links": [
            "https://www.linkedin.com/jobs/data-scientist-jobs",
            "https://www.indeed.com/q-Data-Scientist-jobs.html"
        ],
        "roadmap": {
            "steps": ["Learn Python & Statistics", "Master Pandas, NumPy, Matplotlib", "Study ML Algorithms", "Explore Deep Learning", "Build Projects & Join Competitions"],
            "tools": ["Python, Jupyter Notebook, scikit-learn, TensorFlow, SQL"],
            "certifications": ["Coursera ML, IBM Data Science Professional Certificate"],
            "roles_salary": ["Junior Data Scientist ($70k)", "Data Analyst ($65k)", "Senior Data Scientist ($110k)"]
        }
    },
    "Cloud Computing": {
        "keywords": ["aws", "azure", "google cloud", "terraform", "kubernetes", "docker", "cloud security", "devops", "ci/cd", "cloud architecture"],
        "company": "Amazon, Microsoft, Google, Accenture",
        "role": "Cloud Engineer",
        "learning": "AWS Certification, Google Cloud Training",
        "job_links": [
            "https://www.linkedin.com/jobs/cloud-engineer-jobs",
            "https://www.indeed.com/q-Cloud-Engineer-jobs.html"
        ],
        "roadmap": {
            "steps": ["Learn Cloud Platforms (AWS, GCP, Azure)", "Understand Cloud Services (Compute, Storage, Networking)", "Learn Infrastructure as Code (Terraform, Ansible)", "Master Kubernetes and Containers", "Work on Cloud Security"],
            "tools": ["AWS, Azure, Terraform, Docker, Kubernetes, Jenkins"],
            "certifications": ["AWS Certified Solutions Architect, Google Cloud Professional Architect"],
            "roles_salary": ["Cloud Engineer ($85k)", "Cloud Solutions Architect ($120k)", "Cloud DevOps Engineer ($100k)"]
        }
    },
    "Cybersecurity": {
        "keywords": ["network security", "firewalls", "penetration testing", "ethical hacking", "encryption", "cyber threat analysis", "incident response", "cyber defense", "linux", "siem"],
        "company": "Cisco, Crowdstrike, Palo Alto, Symantec",
        "role": "Cybersecurity Analyst",
        "learning": "Cybrary, CompTIA Security+, EC-Council Certifications",
        "job_links": [
            "https://www.linkedin.com/jobs/cybersecurity-analyst-jobs",
            "https://www.indeed.com/q-Cybersecurity-Analyst-jobs.html"
        ],
        "roadmap": {
            "steps": ["Learn Networking Basics", "Study Ethical Hacking and Penetration Testing", "Understand Security Protocols and Encryption", "Work with SIEM Tools", "Obtain Cybersecurity Certifications"],
            "tools": ["Wireshark, Kali Linux, Metasploit, Burp Suite, Splunk"],
            "certifications": ["CompTIA Security+, EC-Council CEH, CISSP"],
            "roles_salary": ["Cybersecurity Analyst ($70k)", "Penetration Tester ($95k)", "Cybersecurity Engineer ($120k)"]
        }
    },
    "UI/UX Designer": {
        "keywords": ["user interface", "user experience", "figma", "sketch", "adobe xd", "prototyping", "wireframing", "interaction design", "visual design"],
        "company": "Apple, Adobe, IBM, Microsoft, startups",
        "role": "UI/UX Designer",
        "learning": "Coursera UI/UX Design, Design Thinking, Figma Learning",
        "job_links": [
            "https://www.linkedin.com/jobs/ui-ux-designer-jobs",
            "https://www.indeed.com/q-UI-UX-Designer-jobs.html"
        ],
        "roadmap": {
            "steps": ["Learn Design Principles", "Master UI Design Tools (Figma, Sketch)", "Learn User Research & Testing", "Explore Prototyping & Wireframing", "Build Portfolio & Get Feedback"],
            "tools": ["Figma, Adobe XD, Sketch, InVision, Balsamiq"],
            "certifications": ["Google UX Design Certificate, Coursera UI/UX Design Specialization"],
            "roles_salary": ["Junior UI/UX Designer ($60k)", "UI/UX Designer ($85k)", "Senior UI/UX Designer ($110k)"]
        }
    },
    # Add any other domain-specific details here if required
}

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text.lower()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return "No file part"
    file = request.files['resume']
    if file.filename == '':
        return "No selected file"
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    resume_text = extract_text_from_pdf(filepath)
    doc = nlp(resume_text)

    results = []

    for domain, info in career_domains.items():
        match_count = sum(resume_text.count(keyword) for keyword in info["keywords"])
        score = round((match_count / len(info["keywords"])) * 100, 2)
        if score > 0:
            known_skills = [kw for kw in info["keywords"] if kw in resume_text]
            unknown_skills = [kw for kw in info["keywords"] if kw not in resume_text]
            progress = int((len(known_skills) / len(info["keywords"])) * 100)

            results.append({
                "domain": domain,
                "score": score,
                "company": info["company"],
                "role": info["role"],
                "learning": info["learning"],
                "job_links": info["job_links"],
                "known_skills": known_skills,
                "unknown_skills": unknown_skills,
                "progress": progress,
                "roadmap": info.get("roadmap", {})
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return render_template('result.html', results=results)

if __name__ == '__main__':
    print("🔥 Starting AI Career Companion...")
    app.run(debug=True, port=5000)

