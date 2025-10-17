import google.generativeai as genai
import PyPDF2
import re
import os
import os.path as pathing
import pandas as pd
api_key=os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
upload_folder="uploads"
if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

def extract_frm_pdf(file_path):
    content=""
    reader=PyPDF2.PdfReader(file_path)
    for p in reader.pages:
            text=p.extract_text()
            if text:
                 content+=text+"\n"
    return content
    

def extract_frm_csv(file_path):
    df=pd.read_csv(file_path)
    return " ".join(df.astype(str).values.flatten())


def resume_analyse(resume,job_des="IT/software/testing related"):
    predefined_prompt=f"""
    You are an ATS Resume Analyzer.
    Candidate Resume:{resume}
    Job Role: {job_des}

    1. Give an ATS score out of 100.
    2. Suggest improvements in bullet points.
    """

    model=genai.GenerativeModel("gemini-2.0-flash")
    response=model.generate_content(predefined_prompt)
    final_analysis=response.text


    ats_score=0
    match=re.search(r"(\d{1,3})",final_analysis)
    if match:
        ats_score=min(int(match.group(1)),100)
    

    return ats_score,final_analysis

def handle_resume_analyser(file,user_id,mysql):
    file_path=pathing.join(upload_folder,file.filename)
    file.save(file_path)

    if file.filename.endswith(".pdf"):
        resume_text=extract_frm_pdf(file_path)
    elif file.filename.startswith(".csv"):
        resume_text=extract_frm_csv(file_path)
    else:
        raise ValueError("Only PDF and CSV files are supported")
    
    ats,analyse_result=resume_analyse(resume_text)
    

    cur=mysql.connection.cursor()
    cur.execute(
        "insert into resumes(user_id,filename,ats_score,suggestions)values(%s,%s,%s,%s)",
        (user_id,file.filename,ats,analyse_result)
    )
    mysql.connection.commit()
    cur.close()
    return ats,analyse_result