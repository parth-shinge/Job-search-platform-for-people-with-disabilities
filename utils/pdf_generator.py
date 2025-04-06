from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from reportlab.lib.units import inch

def generate_resume_pdf(resume_data, template_function):
    """Generate a PDF resume using the provided data and template"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Add custom styles
    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        textColor=colors.HexColor("#4B8BBE")
    ))
    styles.add(ParagraphStyle(
        name='CustomSubHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        textColor=colors.HexColor("#306998")
    ))
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['BodyText'],
        fontSize=12,
        spaceAfter=10
    ))
    
    # Generate content using template
    story = template_function(resume_data, styles)
    
    # Build PDF
    doc.build(story)
    
    # Get PDF content
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf

def get_template_1(resume_data, styles):
    """Generate resume content for template 1"""
    story = []
    
    # Personal Information and Education on the left side
    left_side = []
    personal_info = resume_data['personal_info']
    
    # Add picture if available
    if 'picture' in personal_info and personal_info['picture']:
        image = Image(BytesIO(personal_info['picture']), width=1.5*inch, height=1.5*inch)
        left_side.append(image)
        left_side.append(Spacer(1, 12))
    
    left_side.append(Paragraph(f"{personal_info['first_name']} {personal_info['last_name']}", styles['CustomHeading']))
    left_side.append(Paragraph(f"Email: {personal_info['email']}", styles['CustomBody']))
    left_side.append(Paragraph(f"Phone: {personal_info['phone']}", styles['CustomBody']))
    left_side.append(Paragraph(f"Location: {personal_info['location']}", styles['CustomBody']))
    if personal_info['linkedin']:
        left_side.append(Paragraph(f"LinkedIn: {personal_info['linkedin']}", styles['CustomBody']))
    left_side.append(Spacer(1, 12))
    
    left_side.append(Paragraph("Education", styles['CustomSubHeading']))
    for edu in resume_data['education']:
        left_side.append(Paragraph(f"{edu['degree']} from {edu['institution']}", styles['CustomBody']))
        left_side.append(Paragraph(f"Graduation Date: {edu['graduation_date']}", styles['CustomBody']))
        left_side.append(Spacer(1, 12))
    
    # Professional Summary, Work Experience, and Skills on the right side
    right_side = []
    right_side.append(Paragraph("Professional Summary", styles['CustomSubHeading']))
    right_side.append(Paragraph(resume_data['summary'], styles['CustomBody']))
    right_side.append(Spacer(1, 12))
    
    right_side.append(Paragraph("Work Experience", styles['CustomSubHeading']))
    for exp in resume_data['experiences']:
        right_side.append(Paragraph(f"{exp['position']} at {exp['company']}", styles['CustomBody']))
        right_side.append(Paragraph(f"{exp['start_date']} - {exp['end_date']}", styles['CustomBody']))
        right_side.append(Paragraph(exp['description'], styles['CustomBody']))
        right_side.append(Spacer(1, 12))
    
    right_side.append(Paragraph("Skills", styles['CustomSubHeading']))
    skills = ', '.join(resume_data['skills'])
    right_side.append(Paragraph(skills, styles['CustomBody']))
    
    # Create a table with two columns
    table_data = [
        [left_side, right_side]
    ]
    table = Table(table_data, colWidths=[2.5 * inch, 4.5 * inch])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (1, 0), (1, -1), colors.whitesmoke),
    ]))
    
    story.append(table)
    
    return story

def get_template_2(resume_data, styles):
    """Generate resume content for template 2"""
    story = []
    
    # Personal Information and Education on the left side
    left_side = []
    personal_info = resume_data['personal_info']
    
    # Add picture if available
    if 'picture' in personal_info and personal_info['picture']:
        image = Image(BytesIO(personal_info['picture']), width=1.5*inch, height=1.5*inch)
        left_side.append(image)
        left_side.append(Spacer(1, 12))
    
    left_side.append(Paragraph(f"{personal_info['first_name']} {personal_info['last_name']}", styles['CustomHeading']))
    left_side.append(Paragraph(f"Email: {personal_info['email']}", styles['CustomBody']))
    left_side.append(Paragraph(f"Phone: {personal_info['phone']}", styles['CustomBody']))
    left_side.append(Paragraph(f"Location: {personal_info['location']}", styles['CustomBody']))
    if personal_info['linkedin']:
        left_side.append(Paragraph(f"LinkedIn: {personal_info['linkedin']}", styles['CustomBody']))
    left_side.append(Spacer(1, 12))
    
    left_side.append(Paragraph("Education", styles['CustomSubHeading']))
    for edu in resume_data['education']:
        left_side.append(Paragraph(f"{edu['degree']} from {edu['institution']}", styles['CustomBody']))
        left_side.append(Paragraph(f"Graduation Date: {edu['graduation_date']}", styles['CustomBody']))
        left_side.append(Spacer(1, 12))
    
    # Professional Summary, Work Experience, and Skills on the right side
    right_side = []
    right_side.append(Paragraph("Professional Summary", styles['CustomSubHeading']))
    right_side.append(Paragraph(resume_data['summary'], styles['CustomBody']))
    right_side.append(Spacer(1, 12))
    
    right_side.append(Paragraph("Work Experience", styles['CustomSubHeading']))
    for exp in resume_data['experiences']:
        right_side.append(Paragraph(f"{exp['position']} at {exp['company']}", styles['CustomBody']))
        right_side.append(Paragraph(f"{exp['start_date']} - {exp['end_date']}", styles['CustomBody']))
        right_side.append(Paragraph(exp['description'], styles['CustomBody']))
        right_side.append(Spacer(1, 12))
    
    right_side.append(Paragraph("Skills", styles['CustomSubHeading']))
    skills = ', '.join(resume_data['skills'])
    right_side.append(Paragraph(skills, styles['CustomBody']))
    
    # Create a table with two columns
    table_data = [
        [left_side, right_side]
    ]
    table = Table(table_data, colWidths=[2.5 * inch, 4.5 * inch])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (1, 0), (1, -1), colors.whitesmoke),
    ]))
    
    story.append(table)
    
    return story