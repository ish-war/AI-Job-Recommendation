import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.resume_parser import ResumeParser
# Debug/Test
if __name__ == "__main__":
    parser = ResumeParser()
    with open("sample_resume.pdf", "rb") as f:
        details = parser.extract_from_resume(f)
        print(details)
