import json
import os
import re

jsonl_path = r'c:/Users/S.Shibukawa/.gemini/antigravity/scratch/rm_researchers20251203.jsonl'
profile_path = r'c:/Users/S.Shibukawa/.gemini/antigravity/scratch/profile.txt'
output_path = r'c:/Users/S.Shibukawa/.gemini/antigravity/scratch/data.js'

# Read profile.txt to extract Lab Members and Awards
def parse_profile_txt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract Lab Members
    lab_members = {
        "collaborators": [],
        "masters": [],
        "undergraduates": []
    }
    
    # Extract collaborators (hardcoded format to preserve beautiful rendering)
    lab_members["collaborators"] = [
        {
            "name_ja": "吉丸 大輔",
            "name_en": "Daisuke Yoshimaru",
            "affiliation": "Jikei University School of Medicine, Division of Regenerative Medicine<br>Department of Radiology, Tokyo Medical University",
            "url": "https://researchmap.jp/D_maru"
        },
        {
            "name_ja": "臼井 圭介",
            "name_en": "Keisuke Usui",
            "affiliation": "Faculty of Health Science, Department of Radiological Technology, Juntendo University"
        },
        {
            "name_ja": "林 直弥",
            "name_en": "Naoya Hayashi",
            "affiliation": "Department of Radiology, Tokyo Medical University"
        }
    ]
    
    # Extract Master's students
    masters_match = re.search(r"Master's Course\n(.*?)\n\nUndergraduate", content, re.DOTALL)
    if masters_match:
        masters_text = masters_match.group(1).strip()
        for line in masters_text.split('\n'):
            if line.strip():
                lab_members["masters"].append(line.strip())
    
    # Extract Undergraduate students
    undergrad_match = re.search(r'Undergraduate student\n(.*?)\n\nAwards:', content, re.DOTALL)
    if undergrad_match:
        undergrad_text = undergrad_match.group(1).strip()
        for line in undergrad_text.split('\n'):
            if line.strip():
                lab_members["undergraduates"].append(line.strip())
    
    # Extract Awards
    awards = []
    awards_match = re.search(r'Awards:\n(.*?)\n\nResearch Interests:', content, re.DOTALL)
    if not awards_match:
        awards_match = re.search(r'Awards:\n(.*?)\n\n\nPublications:', content, re.DOTALL)
    
    if awards_match:
        awards_text = awards_match.group(1).strip()
        current_award = []
        for line in awards_text.split('\n'):
            line = line.strip()
            if line:
                current_award.append(line)
                if len(current_award) == 2:  # Award has 2 lines: description and recipient
                    awards.append(' '.join(current_award))
                    current_award = []
                    
    # Extract Publications
    pubs = {
        "international_journals": [],
        "domestic_journals": [],
        "books": [],
        "domestic_conferences": [],
        "international_conferences": []
    }
    
    pub_match = re.search(r'Publications:\n(.*)', content, re.DOTALL)
    if pub_match:
        pub_text = pub_match.group(1)
        current_category = None
        for line in pub_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('原著論文(国際)'):
                current_category = 'international_journals'
            elif line.startswith('原著論文(国内)'):
                current_category = 'domestic_journals'
            elif line.startswith('著書'):
                current_category = 'books'
            elif line.startswith('国内学会'):
                current_category = 'domestic_conferences'
            elif line.startswith('国際学会'):
                current_category = 'international_conferences'
            elif current_category:
                # remove "1.	" or "1. " or "2. "
                text = re.sub(r'^\d+\.\s*', '', line)
                if text:
                    pubs[current_category].append(text)

    return lab_members, awards, pubs

lab_members, awards, manual_publications = parse_profile_txt(profile_path)

manual_profile = {
    "name": {
        "ja": "渋川 周平",
        "en": "Shuhei Shibukawa",
        "kana": "シブカワ シュウヘイ"
    },
    "affiliations": [
        { "ja": "順天堂大学 診療放射線学科 准教授", "en": "Associate Professor, Department of Radiological Sciences, Juntendo University" },
        { "ja": "東京大学 大学院総合文化研究科 特任助教", "en": "Project Assistant Professor, Graduate School of Arts and Sciences, The University of Tokyo" },
        { "ja": "東京医科大学 放射線医学分野 非常勤講師", "en": "Part-time Lecturer, Department of Radiology, Tokyo Medical University" }
    ],
    "keywords": [
        { "ja": "磁気共鳴画像(MRI)", "en": "Magnetic Resonance Imaging (MRI)" },
        { "ja": "骨格筋イメージング", "en": "Skeletal Muscle Imaging" },
        { "ja": "脳画像解析", "en": "Brain Image Analysis" }
    ],
    "lab_members": lab_members,
    "awards": awards
}

data = []
try:
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Error decoding line: {e}")
except Exception as e:
    print(f"Error reading file: {e}")

with open(output_path, 'w', encoding='utf-8') as f:
    f.write("const manualProfile = " + json.dumps(manual_profile, ensure_ascii=False, indent=4) + ";\n\n")
    f.write("const manualPublications = " + json.dumps(manual_publications, ensure_ascii=False, indent=4) + ";\n\n")
    f.write("const researcherData = " + json.dumps(data, ensure_ascii=False, indent=4) + ";\n")

print("data.js regenerated successfully with Lab Members and Awards.")
