from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

def get_template_1(resume_data, styles):
    """Professional template"""
    story = []
    
    # Header
    personal = resume_data['personal_info']
    name = f"{personal['first_name']} {personal['last_name']}"
    story.append(Paragraph(name, styles['CustomHeading']))
    
    contact_info = f"{personal['email']} | {personal['phone']} | {personal['location']}"
    if personal['linkedin']:
        contact_info += f" | {personal['linkedin']}"
    story.append(Paragraph(contact_info, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Summary
    story.append(Paragraph("Professional Summary", styles['Heading2']))
    story.append(Paragraph(resume_data['summary'], styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Experience
    story.append(Paragraph("Experience", styles['Heading2']))
    for exp in resume_data['experiences']:
        story.append(Paragraph(
            f"<b>{exp['position']}</b> at {exp['company']}", 
            styles['Normal']
        ))
        story.append(Paragraph(
            f"{exp['start_date']} - {exp['end_date']}", 
            styles['Normal']
        ))
        story.append(Paragraph(exp['description'], styles['Normal']))
        story.append(Spacer(1, 10))
    
    # Education
    story.append(Paragraph("Education", styles['Heading2']))
    for edu in resume_data['education']:
        story.append(Paragraph(
            f"<b>{edu['degree']}</b> - {edu['institution']}", 
            styles['Normal']
        ))
        story.append(Paragraph(
            f"Graduated: {edu['graduation_date']}", 
            styles['Normal']
        ))
        story.append(Spacer(1, 10))
    
    # Skills
    story.append(Paragraph("Skills", styles['Heading2']))
    skills_text = ", ".join(resume_data['skills'])
    story.append(Paragraph(skills_text, styles['Normal']))
    
    return story

def get_template_2(resume_data, styles):
    """Modern template"""
    story = []
    
    # Header with different styling
    personal = resume_data['personal_info']
    name = f"{personal['first_name']} {personal['last_name']}"
    story.append(Paragraph(name, styles['Title']))
    
    # Two-column layout for contact info
    contact_data = [
        [Paragraph(f"Email: {personal['email']}", styles['Normal']),
         Paragraph(f"Phone: {personal['phone']}", styles['Normal'])],
        [Paragraph(f"Location: {personal['location']}", styles['Normal']),
         Paragraph(f"LinkedIn: {personal['linkedin']}", styles['Normal']) if personal['linkedin'] else None]
    ]
    
    contact_table = Table(contact_data, colWidths=['50%', '50%'])
    contact_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ]))
    story.append(contact_table)
    story.append(Spacer(1, 20))
    
    # Rest of the resume with modern styling
    # (Similar to template 1 but with different styling)
    
    return story
