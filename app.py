import streamlit as st
from fpdf import FPDF

# ------------------- OOP classes -------------------

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.resumes = []

    def create_resume(self, resume):
        self.resumes.append(resume)

class Resume:
    def __init__(self, name, email, skills, education, experience):
        self.name = name
        self.email = email
        self.skills = skills
        self.education = education
        self.experience = experience

class Template:
    def __init__(self, title, fields):
        self.title = title
        self.fields = fields  # Fields like 'name', 'email', etc.


# ------------------ Streamlit app UI -------------------

# Authentication Form
def authenticate():
    st.title("ResumeMint - AI Resume Builder")
    st.subheader("Login to get started")

    username_input = st.text_input("Username").strip().lower()
    password_input = st.text_input("Password", type="password").strip()

    if st.button("Login"):
        # In this case, we create a new user each time, so we skip user validation
        if username_input and password_input:
            user = User(username_input, password_input)  # create a new user instance
            st.session_state.logged_in_user = user
            st.success(f"Welcome back, {username_input}!")
            return user
        else:
            st.error("Please enter a username and password")
            return None

# Resume Builder Form
def build_resume(user):
    st.title("Create Your Resume")
    st.subheader("Fill out the details below:")

    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    skills = st.text_area("Skills (comma-separated)")
    education = st.text_area("Education")
    experience = st.text_area("Work Experience")

    if st.button("Save Resume"):
        resume = Resume(name, email, skills, education, experience)
        user.create_resume(resume)
        st.success(f"Resume for {name} created successfully!")

# Resume PDF Generator
def generate_pdf(resume):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(200, 10, "Resume", ln=True, align="C")

    # Personal Information
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Name: {resume.name}", ln=True)
    pdf.cell(200, 10, f"Email: {resume.email}", ln=True)

    # Skills
    pdf.ln(10)
    pdf.cell(200, 10, "Skills:", ln=True)
    pdf.multi_cell(200, 10, resume.skills)

    # Education
    pdf.ln(10)
    pdf.cell(200, 10, "Education:", ln=True)
    pdf.multi_cell(200, 10, resume.education)

    # Experience
    pdf.ln(10)
    pdf.cell(200, 10, "Experience:", ln=True)
    pdf.multi_cell(200, 10, resume.experience)

    # Output PDF to file
    pdf_output = f"{resume.name}_Resume.pdf"
    pdf.output(pdf_output)
    
    return pdf_output

# Simulate Payment for Download
def simulate_payment():
    if st.button("Pay ₹50 to Download Resume"):
        st.success("Payment Successful! Downloading your resume...")
        return True
    return False

# Main app logic
def main():
    if 'logged_in_user' not in st.session_state:
        user = authenticate()
        if not user:
            return
    else:
        user = st.session_state.logged_in_user

    if user:
        build_resume(user)

        if len(user.resumes) > 0:
            if simulate_payment():
                resume = user.resumes[-1]
                resume_pdf = generate_pdf(resume)
                with open(resume_pdf, "rb") as file:
                    st.download_button(
                        label="Download Resume",
                        data=file,
                        file_name=resume_pdf,
                        mime="application/pdf"
                    )

if __name__ == "__main__":
    main()


