"""
Export utilities for DataAnalytics Vietnam
Generate professional PDF and PowerPoint reports
"""

import io
import base64
from datetime import datetime
from typing import Dict, List, Any
import plotly.graph_objects as go


def export_to_pdf(result: Dict[str, Any], df: Any, lang: str = "vi") -> bytes:
    """
    Export analysis results to professional PDF report
    
    Args:
        result: Pipeline result dictionary
        df: Original dataframe
        lang: Language code ('vi' or 'en')
    
    Returns:
        PDF file as bytes
    """
    try:
        from reportlab.lib.pagesizes import A4, letter
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
        from reportlab.pdfgen import canvas
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1E40AF'),
            spaceAfter=12,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1E40AF'),
            spaceAfter=10
        )
        
        # Build PDF content
        content = []
        
        # Title
        if lang == "vi":
            title = Paragraph("📊 BÁO CÁO PHÂN TÍCH DỮ LIỆU", title_style)
            subtitle = Paragraph("DataAnalytics Vietnam - Professional Business Intelligence", styles['Normal'])
        else:
            title = Paragraph("📊 DATA ANALYSIS REPORT", title_style)
            subtitle = Paragraph("DataAnalytics Vietnam - Professional Business Intelligence", styles['Normal'])
        
        content.append(title)
        content.append(subtitle)
        content.append(Spacer(1, 0.3*inch))
        
        # Report metadata
        metadata_data = [
            ["Report Date" if lang == "en" else "Ngày báo cáo", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["Domain" if lang == "en" else "Ngành nghề", result['domain_info']['domain_name']],
            ["Expert Perspective" if lang == "en" else "Góc nhìn chuyên gia", result['domain_info']['expert_role'][:60]],
            ["Processing Time" if lang == "en" else "Thời gian xử lý", f"{result['performance']['total']:.1f}s"],
            ["Quality Score" if lang == "en" else "Điểm chất lượng", f"{result['quality_scores']['overall']:.0f}/100"]
        ]
        
        metadata_table = Table(metadata_data, colWidths=[2.5*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F8FAFC')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1E293B')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0'))
        ]))
        
        content.append(metadata_table)
        content.append(Spacer(1, 0.4*inch))
        
        # Executive Summary
        content.append(Paragraph("📋 Executive Summary" if lang == "en" else "📋 Tóm Tắt Điều Hành", heading_style))
        summary_text = result['insights'].get('executive_summary', 'No summary available')
        content.append(Paragraph(summary_text, styles['Normal']))
        content.append(Spacer(1, 0.3*inch))
        
        # Key KPIs
        content.append(Paragraph("📈 Key Performance Indicators" if lang == "en" else "📈 Chỉ Số Hiệu Suất Chính", heading_style))
        
        kpis = result['dashboard'].get('kpis', {})
        if kpis:
            kpi_data = [["KPI", "Value" if lang == "en" else "Giá trị", "Status" if lang == "en" else "Trạng thái", "Benchmark" if lang == "en" else "Chuẩn"]]
            
            for kpi_name, kpi_info in list(kpis.items())[:10]:  # Top 10 KPIs
                kpi_data.append([
                    kpi_name,
                    f"{kpi_info['value']:.1f}",
                    kpi_info.get('status', 'N/A'),
                    str(kpi_info.get('benchmark', 'N/A'))
                ])
            
            kpi_table = Table(kpi_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            kpi_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E40AF')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
            ]))
            
            content.append(kpi_table)
        
        content.append(Spacer(1, 0.3*inch))
        
        # Key Insights
        content.append(Paragraph("🎯 Key Insights" if lang == "en" else "🎯 Insights Chính", heading_style))
        
        for i, insight in enumerate(result['insights'].get('key_insights', [])[:5], 1):
            impact_emoji = "🔴" if insight['impact'] == 'high' else "🟡" if insight['impact'] == 'medium' else "🟢"
            insight_text = f"{impact_emoji} <b>{insight['title']}</b><br/>{insight['description']}"
            content.append(Paragraph(insight_text, styles['Normal']))
            content.append(Spacer(1, 0.15*inch))
        
        content.append(PageBreak())
        
        # Recommendations
        content.append(Paragraph("🚀 Recommendations" if lang == "en" else "🚀 Khuyến Nghị", heading_style))
        
        for i, rec in enumerate(result['insights'].get('recommendations', [])[:5], 1):
            priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
            rec_text = f"{priority_emoji} <b>[{rec['priority'].upper()}] {rec['action']}</b><br/>Expected Impact: {rec['expected_impact']}<br/>Timeline: {rec['timeline']}"
            content.append(Paragraph(rec_text, styles['Normal']))
            content.append(Spacer(1, 0.15*inch))
        
        # Charts (convert to images)
        content.append(PageBreak())
        content.append(Paragraph("📊 Visual Analysis" if lang == "en" else "📊 Phân Tích Trực Quan", heading_style))
        
        charts = result['dashboard']['charts']
        for i, chart in enumerate(charts[:6]):  # First 6 charts
            try:
                # Convert Plotly chart to image
                img_bytes = chart['figure'].to_image(format="png", width=700, height=400)
                img = Image(io.BytesIO(img_bytes), width=6*inch, height=3.5*inch)
                content.append(img)
                content.append(Spacer(1, 0.2*inch))
                
                if (i + 1) % 2 == 0 and i < len(charts) - 1:
                    content.append(PageBreak())
            except Exception as e:
                content.append(Paragraph(f"[Chart {i+1}: Image generation failed]", styles['Normal']))
        
        # Footer
        content.append(Spacer(1, 0.5*inch))
        footer_text = "Generated by DataAnalytics Vietnam | www.dataanalytics.vn | ISO 8000 Compliant"
        content.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)))
        
        # Build PDF
        doc.build(content)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    except ImportError:
        raise ImportError("reportlab library required. Install: pip install reportlab kaleido")
    except Exception as e:
        raise Exception(f"PDF export failed: {str(e)}")


def export_to_powerpoint(result: Dict[str, Any], df: Any, lang: str = "vi") -> bytes:
    """
    Export analysis results to professional PowerPoint presentation
    
    Args:
        result: Pipeline result dictionary
        df: Original dataframe
        lang: Language code ('vi' or 'en')
    
    Returns:
        PowerPoint file as bytes
    """
    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.enum.text import PP_ALIGN
        from pptx.dml.color import RGBColor
        
        # Create presentation
        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)
        
        # Slide 1: Title
        slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
        
        # Add title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(1))
        title_frame = title_box.text_frame
        title_para = title_frame.add_paragraph()
        title_para.text = "📊 DATA ANALYSIS REPORT" if lang == "en" else "📊 BÁO CÁO PHÂN TÍCH DỮ LIỆU"
        title_para.font.size = Pt(44)
        title_para.font.bold = True
        title_para.font.color.rgb = RGBColor(30, 64, 175)  # #1E40AF
        title_para.alignment = PP_ALIGN.CENTER
        
        # Add subtitle
        subtitle_box = slide.shapes.add_textbox(Inches(1), Inches(3.5), Inches(8), Inches(0.5))
        subtitle_frame = subtitle_box.text_frame
        subtitle_para = subtitle_frame.add_paragraph()
        subtitle_para.text = "DataAnalytics Vietnam - Professional Business Intelligence"
        subtitle_para.font.size = Pt(18)
        subtitle_para.font.color.rgb = RGBColor(100, 116, 139)
        subtitle_para.alignment = PP_ALIGN.CENTER
        
        # Add date
        date_box = slide.shapes.add_textbox(Inches(1), Inches(6), Inches(8), Inches(0.5))
        date_frame = date_box.text_frame
        date_para = date_frame.add_paragraph()
        date_para.text = datetime.now().strftime("%B %d, %Y")
        date_para.font.size = Pt(14)
        date_para.font.color.rgb = RGBColor(100, 116, 139)
        date_para.alignment = PP_ALIGN.CENTER
        
        # Slide 2: Executive Summary
        slide = prs.slides.add_slide(prs.slide_layouts[1])  # Title and Content
        title = slide.shapes.title
        title.text = "📋 Executive Summary" if lang == "en" else "📋 Tóm Tắt Điều Hành"
        
        content = slide.placeholders[1]
        tf = content.text_frame
        tf.clear()
        
        summary = result['insights'].get('executive_summary', 'No summary available')
        p = tf.add_paragraph()
        p.text = summary
        p.font.size = Pt(16)
        p.level = 0
        
        # Slide 3: Key KPIs
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        title = slide.shapes.title
        title.text = "📈 Key Performance Indicators" if lang == "en" else "📈 Chỉ Số Hiệu Suất Chính"
        
        kpis = result['dashboard'].get('kpis', {})
        if kpis:
            # Add KPIs as table
            rows = min(6, len(kpis)) + 1  # Header + max 6 KPIs
            cols = 4
            
            left = Inches(1)
            top = Inches(2)
            width = Inches(8)
            height = Inches(4)
            
            table = slide.shapes.add_table(rows, cols, left, top, width, height).table
            
            # Header row
            table.cell(0, 0).text = "KPI"
            table.cell(0, 1).text = "Value" if lang == "en" else "Giá trị"
            table.cell(0, 2).text = "Status" if lang == "en" else "Trạng thái"
            table.cell(0, 3).text = "Benchmark" if lang == "en" else "Chuẩn"
            
            # KPI data
            for i, (kpi_name, kpi_info) in enumerate(list(kpis.items())[:6], 1):
                table.cell(i, 0).text = kpi_name
                table.cell(i, 1).text = f"{kpi_info['value']:.1f}"
                table.cell(i, 2).text = kpi_info.get('status', 'N/A')
                table.cell(i, 3).text = str(kpi_info.get('benchmark', 'N/A'))
        
        # Slides 4+: Charts
        charts = result['dashboard']['charts']
        for i, chart in enumerate(charts[:8]):  # Max 8 charts
            slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title only
            title = slide.shapes.title
            title.text = f"📊 Chart {i+1}: {chart.get('title', 'Analysis')}"
            
            try:
                # Convert chart to image
                img_bytes = chart['figure'].to_image(format="png", width=1000, height=600)
                img_stream = io.BytesIO(img_bytes)
                
                # Add image to slide
                left = Inches(1)
                top = Inches(1.5)
                pic = slide.shapes.add_picture(img_stream, left, top, width=Inches(8))
            except Exception as e:
                # Add error text if image generation fails
                text_box = slide.shapes.add_textbox(Inches(2), Inches(3), Inches(6), Inches(1))
                tf = text_box.text_frame
                p = tf.add_paragraph()
                p.text = f"[Chart image generation failed: {str(e)}]"
                p.font.size = Pt(14)
        
        # Slide: Key Insights
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        title = slide.shapes.title
        title.text = "🎯 Key Insights" if lang == "en" else "🎯 Insights Chính"
        
        content = slide.placeholders[1]
        tf = content.text_frame
        tf.clear()
        
        for insight in result['insights'].get('key_insights', [])[:5]:
            impact_emoji = "🔴" if insight['impact'] == 'high' else "🟡" if insight['impact'] == 'medium' else "🟢"
            p = tf.add_paragraph()
            p.text = f"{impact_emoji} {insight['title']}"
            p.font.size = Pt(14)
            p.font.bold = True
            p.level = 0
            
            p2 = tf.add_paragraph()
            p2.text = insight['description']
            p2.font.size = Pt(12)
            p2.level = 1
        
        # Slide: Recommendations
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        title = slide.shapes.title
        title.text = "🚀 Recommendations" if lang == "en" else "🚀 Khuyến Nghị"
        
        content = slide.placeholders[1]
        tf = content.text_frame
        tf.clear()
        
        for rec in result['insights'].get('recommendations', [])[:5]:
            priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
            p = tf.add_paragraph()
            p.text = f"{priority_emoji} [{rec['priority'].upper()}] {rec['action']}"
            p.font.size = Pt(14)
            p.font.bold = True
            p.level = 0
            
            p2 = tf.add_paragraph()
            p2.text = f"Expected Impact: {rec['expected_impact']} | Timeline: {rec['timeline']}"
            p2.font.size = Pt(11)
            p2.level = 1
        
        # Final Slide: Thank You
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        thank_you_box = slide.shapes.add_textbox(Inches(2), Inches(3), Inches(6), Inches(1))
        tf = thank_you_box.text_frame
        p = tf.add_paragraph()
        p.text = "Thank You!" if lang == "en" else "Cảm ơn!"
        p.font.size = Pt(48)
        p.font.bold = True
        p.font.color.rgb = RGBColor(30, 64, 175)
        p.alignment = PP_ALIGN.CENTER
        
        footer_box = slide.shapes.add_textbox(Inches(1), Inches(6), Inches(8), Inches(0.5))
        tf = footer_box.text_frame
        p = tf.add_paragraph()
        p.text = "DataAnalytics Vietnam | www.dataanalytics.vn | ISO 8000 Compliant"
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(100, 116, 139)
        p.alignment = PP_ALIGN.CENTER
        
        # Save to bytes
        ppt_buffer = io.BytesIO()
        prs.save(ppt_buffer)
        ppt_bytes = ppt_buffer.getvalue()
        ppt_buffer.close()
        
        return ppt_bytes
    
    except ImportError:
        raise ImportError("python-pptx library required. Install: pip install python-pptx kaleido")
    except Exception as e:
        raise Exception(f"PowerPoint export failed: {str(e)}")


def create_shareable_link(result: Dict[str, Any], df: Any) -> str:
    """
    Create shareable link for report (placeholder for future implementation)
    
    Args:
        result: Pipeline result
        df: Original dataframe
    
    Returns:
        Shareable URL
    """
    # TODO: Implement cloud storage and link generation
    # For now, return placeholder
    return "https://dataanalytics.vn/reports/[REPORT_ID]"


def send_report_email(email: str, report_bytes: bytes, format: str = "pdf", lang: str = "vi") -> bool:
    """
    Send report via email (placeholder for future implementation)
    
    Args:
        email: Recipient email
        report_bytes: Report file bytes
        format: 'pdf' or 'pptx'
        lang: Language code
    
    Returns:
        Success boolean
    """
    # TODO: Implement email sending with SMTP
    # For now, return placeholder
    return True
