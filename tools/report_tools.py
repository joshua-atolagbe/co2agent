"""
Tools for generating and saving reports in PDF format using ReportLab with proper CO₂ subscript
and two-column layout.
"""

import os
import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    ListFlowable, ListItem, PageBreak, Frame, PageTemplate, NextPageTemplate,
    FrameBreak, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

def get_styles():
    """
    Create a fresh document styles for each call.
    
    Returns:
        Dict: Dictionary of styled objects
    """
    # Create a fresh copy of the sample stylesheet
    styles = getSampleStyleSheet()
    
    # Create all custom styles without reusing names
    custom_title = ParagraphStyle(
        name='CustomReportTitle', 
        parent=styles['Heading1'], 
        fontSize=20, 
        alignment=1,  # center
        spaceAfter=0.3*inch
    )
    
    custom_subtitle = ParagraphStyle(
        name='CustomReportSubtitle', 
        parent=styles['Heading2'], 
        fontSize=14, 
        alignment=1,  # center
        spaceAfter=0.2*inch
    )
    
    section_title = ParagraphStyle(
        name='CustomSectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=0.2*inch,
        spaceAfter=0.1*inch
    )
    
    subsection_title = ParagraphStyle(
        name='CustomSubsectionTitle',
        parent=styles['Heading3'],
        fontSize=12,
        spaceBefore=0.15*inch,
        spaceAfter=0.1*inch
    )
    
    body_text = ParagraphStyle(
        name='CustomBodyText',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=0.1*inch,
        leading=14
    )
    
    # Add the styles to the stylesheet
    styles.add(custom_title)
    styles.add(custom_subtitle)
    styles.add(section_title)
    styles.add(subsection_title)
    styles.add(body_text)
    
    # Create a style mapping for easier reference
    style_map = {
        'CustomTitle': custom_title,
        'CustomSubtitle': custom_subtitle,
        'SectionTitle': section_title,
        'SubsectionTitle': subsection_title,
        'BodyText': body_text,
        'Heading3': styles['Heading3'],
        'Heading4': styles['Heading4']
    }
    
    return style_map

def save_co2_report_to_pdf(report_content: str, well_name: str = "Well") -> str:
    """
    Save the generated CO₂ storage assessment report to a PDF file with correct markdown formatting,
    CO₂ subscript, and two-column layout.

    Args:
        report_content (str): The text content of the report in markdown format
        well_name (str): Name of the well for filename

    Returns:
        str: Path to the saved PDF file
    """
    reports_dir = "co2_assessment_reports"
    os.makedirs(reports_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_well_name = re.sub(r'[^\w]', '_', well_name)
    filename = f"{reports_dir}/CO2_Storage_Assessment_{sanitized_well_name}_{timestamp}.pdf"

    # Get page dimensions
    page_width, page_height = landscape(A4)
    
    # Create a single-column frame for the title page
    title_frame = Frame(
        2*cm,  # x
        2*cm,  # y
        page_width - 4*cm,  # width
        page_height - 4*cm,  # height
        id='title'
    )
    
    # Create frames for two-column layout with better spacing
    col_width = (page_width - 5*cm) / 2  # Allow for margins and gutter
    col_height = page_height - 4*cm

    frame1 = Frame(
        2*cm,  # Left margin
        2*cm,  # Bottom margin
        col_width,  # Width
        col_height,  # Height
        id='col1',
        showBoundary=0  # Set to 1 for debugging
    )

    frame2 = Frame(
        3*cm + col_width,  # Start after first column + gutter
        2*cm,  # Bottom margin
        col_width,  # Width
        col_height,  # Height
        id='col2',
        showBoundary=0  # Set to 1 for debugging
    )
    
    # Create page templates with proper IDs
    title_template = PageTemplate(id='title', frames=[title_frame])
    two_column_template = PageTemplate(id='two_column', frames=[frame1, frame2])
    
    # Setup document
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(A4),
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Replace all instances of CO2 with proper CO₂ subscript
    report_content = re.sub(r'CO2', 'CO₂', report_content)
    report_content = apply_styling_enhancements(report_content)
    
    # Process content and build the PDF
    elements = _process_markdown_content(report_content, well_name)
    
    # Add page template instructions
    elements.insert(0, NextPageTemplate('title'))
    
    # Add a page break and switch to two-column layout after the title page
    title_page_end_index = _find_title_page_end(elements)
    if title_page_end_index > 0:
        elements.insert(title_page_end_index, PageBreak())
        elements.insert(title_page_end_index + 1, NextPageTemplate('two_column'))
        
        # Make sure FrameBreak is added between sections to flow to next column
        for i in range(title_page_end_index + 2, len(elements)):
            if isinstance(elements[i], Paragraph) and hasattr(elements[i], 'style') and elements[i].style.name == 'CustomSectionTitle':
                # Add FrameBreak before major sections to ensure they start in a new column if needed
                elements.insert(i, FrameBreak())
    
    # Build the document with the templates
    doc.addPageTemplates([title_template, two_column_template])
    doc.build(elements)
    
    print(f"Report saved to {filename}")
    return filename

def _find_title_page_end(elements: List[Any]) -> int:
    """Find where to end the title page, usually after executive summary."""
    for i, element in enumerate(elements):
        if isinstance(element, Paragraph) and "Introduction" in element.text:
            return i
    # If no introduction found, default to after a few elements
    return min(10, len(elements))

def _process_markdown_content(report_content: str, well_name: str) -> List[Any]:
    """
    Convert markdown content to ReportLab elements.
    
    Args:
        report_content (str): Report content in markdown format
        well_name (str): Name of the well for title
        
    Returns:
        list: List of ReportLab flowable elements
    """
    # Get fresh styles
    styles = get_styles()
    
    # Create the elements list
    elements = []
    
    # Add title and timestamp
    elements.append(Paragraph(f"CO₂ Storage Assessment Report: {well_name}", styles['CustomTitle']))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['CustomSubtitle']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Process the markdown content
    lines = report_content.strip().split('\n')
    
    state = {
        'in_table': False,
        'table_data': [],
        'in_list': False,
        'list_items': [],
        'list_type': None
    }
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            if state['in_list']:
                # End of list
                elements.append(_create_list(state['list_items'], state['list_type'], styles))
                state['list_items'] = []
                state['in_list'] = False
                state['list_type'] = None
            i += 1
            continue
        
        # Process the line based on its type
        processed = _process_line(line, state, styles)
        if processed:
            if isinstance(processed, list):
                elements.extend(processed)
            else:
                elements.append(processed)
        i += 1
    
    # Handle any remaining elements
    if state['in_table'] and state['table_data']:
        elements.append(_create_table(state['table_data']))
    
    if state['in_list'] and state['list_items']:
        elements.append(_create_list(state['list_items'], state['list_type'], styles))
    
    return elements

def _process_line(line: str, state: Dict[str, Any], styles: Dict[str, ParagraphStyle]) -> Optional[Any]:
    """
    Process a single line of markdown.
    
    Args:
        line: The line to process
        state: Current parsing state
        styles: Document styles
        
    Returns:
        Optional[Any]: ReportLab element(s) or None if integrated into state
    """
    result = []
    
    # Headers
    if header_match := re.match(r'^(#{1,4})\s+(.+)$', line):
        level = len(header_match.group(1))
        heading_text = header_match.group(2)
        
        if state['in_table']:
            result.append(_create_table(state['table_data']))
            state['in_table'] = False
            state['table_data'] = []
        
        if state['in_list']:
            result.append(_create_list(state['list_items'], state['list_type'], styles))
            state['list_items'] = []
            state['in_list'] = False
            state['list_type'] = None
        
        # Use custom styles for headings
        if level == 1:
            style_name = 'SectionTitle'
        elif level == 2:
            style_name = 'SubsectionTitle'
        else:
            style_name = f'Heading{level}'
            
        # Add a spacer before section headings for better layout
        if level == 1:
            result.append(Spacer(1, 0.2*inch))
            
        result.append(Paragraph(heading_text, styles[style_name]))
        return result
    
    # Lists
    elif list_match := re.match(r'^([-*]|\d+\.)\s+(.+)$', line):
        prefix = list_match.group(1)
        content = list_match.group(2)
        
        if prefix in ['-', '*']:
            list_type = 'bullet'
        else:
            list_type = 'number'
        
        if not state['in_list'] or state['list_type'] != list_type:
            if state['in_list']:
                result.append(_create_list(state['list_items'], state['list_type'], styles))
                state['list_items'] = []
            state['in_list'] = True
            state['list_type'] = list_type
        
        # Process inline formatting in list items
        formatted_content = _process_inline_formatting(content)
        state['list_items'].append(formatted_content)
        return None
    
    # Tables
    elif '|' in line:
        # Skip table separator lines
        if '---' in line:
            return None
            
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        
        if not state['in_table']:
            state['in_table'] = True
            state['table_data'] = []
            # Extract header
            state['table_data'].append(cells)
        elif state['in_table']:
            # Extract row
            state['table_data'].append(cells)
        return None
    
    # Regular paragraph
    else:
        elements_to_add = []
        
        if state['in_table']:
            elements_to_add.append(_create_table(state['table_data']))
            elements_to_add.append(Spacer(1, 0.2*inch))
            state['in_table'] = False
            state['table_data'] = []
        
        if state['in_list']:
            elements_to_add.append(_create_list(state['list_items'], state['list_type'], styles))
            state['list_items'] = []
            state['in_list'] = False
            state['list_type'] = None
        
        # Process inline formatting
        processed_line = _process_inline_formatting(line)
        elements_to_add.append(Paragraph(processed_line, styles['BodyText']))
        
        return elements_to_add

def _process_inline_formatting(text: str) -> str:
    """Process inline markdown formatting properly."""
    # Process bold first (important for nested formatting)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Then process italic
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    
    # Process code blocks
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    
    # Ensure CO2 is properly formatted with subscript
    text = re.sub(r'CO2', r'CO<sub>2</sub>', text)
    
    return text

def _create_table(table_data: List[List[str]]) -> Table:
    """Create a ReportLab Table from table data with proper styling."""
    if not table_data:
        return None
    
    # Process table data to handle any styling
    processed_data = []
    for row in table_data:
        processed_row = [Paragraph(_process_inline_formatting(cell), getSampleStyleSheet()['Normal']) for cell in row]
        processed_data.append(processed_row)
    
    # Calculate appropriate column widths
    col_count = max(len(row) for row in table_data)
    col_width = 7 * cm  # Adjust based on your page width
    
    # Create Table object with specific column widths
    table = Table(processed_data, colWidths=[col_width/col_count] * col_count)
    
    # Apply better styles
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Left alignment is better for readability
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Lighter grid lines
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ])
    
    table.setStyle(style)
    
    # Wrap in KeepTogether to avoid table breaking across columns
    return KeepTogether(table)

def _create_list(items: List[str], list_type: str, styles: Dict[str, ParagraphStyle]) -> ListFlowable:
    """Create a ReportLab ListFlowable from list items with proper formatting."""
    if not items:
        return None
    
    # Create list items with proper paragraph styling to handle formatting
    list_items = [ListItem(Paragraph(item, styles['BodyText'])) for item in items]
    
    bullet_type = 'bullet' if list_type == 'bullet' else '1'
    return ListFlowable(
        list_items,
        bulletType=bullet_type,
        leftIndent=0.5*inch,
        spaceBefore=0.1*inch,
        spaceAfter=0.1*inch
    )

def apply_styling_enhancements(report_content: str) -> str:
    """
    Apply additional styling enhancements to the report content.
    
    Args:
        report_content: The original report content
        
    Returns:
        str: Enhanced report content
    """
    # Replace CO2 with proper CO₂ format
    content = re.sub(r'CO2', r'CO₂', report_content)
    
    # Enhance headings with additional formatting
    content = re.sub(r'^(# .+)$', r'\1\n', content, flags=re.MULTILINE)
    
    # Make sure to handle bold and italic formatting
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', content)
    
    return content