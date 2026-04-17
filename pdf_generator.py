"""
FinanIA - Generador de Reportes PDF
Utiliza reportlab para generar reportes en formato PDF
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

def generar_reporte_usuario_pdf(datos, output_path):
    """Generar reporte PDF para un usuario"""
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#004481'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#004481'),
        spaceAfter=12
    )
    
    # Título
    elements.append(Paragraph("REPORTE FINANCIERO", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Información del usuario
    usuario = datos['usuario']
    fecha_consulta = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    info_data = [
        ['Usuario:', usuario['nombre']],
        ['Email:', usuario['email']],
        ['Fecha de Generación:', fecha_consulta]
    ]
    
    if 'fecha_inicio' in datos and 'fecha_fin' in datos:
        info_data.append(['Período:', f"{datos['fecha_inicio']} - {datos['fecha_fin']}"])
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Resumen Financiero
    elements.append(Paragraph("RESUMEN FINANCIERO", heading_style))
    
    if 'estadisticas_mes_actual' in datos:
        stats = datos['estadisticas_mes_actual']
        resumen_data = [
            ['Concepto', 'Monto'],
            ['Total Gastos', f"${stats.get('total_gastos', 0):.2f}"],
            ['Total Tickets', f"${stats.get('total_tickets', 0):.2f}"],
            ['Total del Mes', f"${stats.get('total_mes', 0):.2f}"],
            ['Total Ahorros', f"${datos.get('total_ahorros', 0):.2f}"],
        ]
    else:
        resumen_data = [
            ['Concepto', 'Monto'],
            ['Total Gastos', f"${datos.get('total_gastos', 0):.2f}"],
            ['Total Tickets', f"${datos.get('total_tickets', 0):.2f}"],
            ['Total Ahorros', f"${datos.get('total_ahorros', 0):.2f}"],
        ]
    
    if 'ingresos_mensuales' in datos:
        resumen_data.append(['Ingresos Mensuales', f"${datos['ingresos_mensuales']:.2f}"])
    
    if 'balance' in datos:
        balance_color = colors.green if datos['balance'] >= 0 else colors.red
        resumen_data.append(['Balance', f"${datos['balance']:.2f}"])
    
    resumen_table = Table(resumen_data, colWidths=[3.5*inch, 2.5*inch])
    resumen_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#004481')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
    ]))
    
    elements.append(resumen_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Gastos por Categoría
    if 'estadisticas_mes_actual' in datos and datos['estadisticas_mes_actual'].get('gastos_por_categoria'):
        elements.append(Paragraph("GASTOS POR CATEGORÍA", heading_style))
        categoria_data = [['Categoría', 'Monto']]
        for cat, monto in datos['estadisticas_mes_actual']['gastos_por_categoria'].items():
            categoria_data.append([cat, f"${monto:.2f}"])
        
        cat_table = Table(categoria_data, colWidths=[3.5*inch, 2.5*inch])
        cat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ffd100')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        elements.append(cat_table)
        elements.append(Spacer(1, 0.3*inch))
    
    # Detalle de Transacciones (si existen)
    if 'gastos' in datos and datos['gastos']:
        elements.append(Paragraph("DETALLE DE GASTOS", heading_style))
        gastos_data = [['Fecha', 'Descripción', 'Categoría', 'Monto']]
        for gasto in datos['gastos'][:20]:  # Limitar a 20 gastos
            fecha = str(gasto['fecha']) if 'fecha' in gasto else ''
            desc = gasto.get('descripcion', '')[:40]
            cat = gasto.get('categoria', '')
            monto = float(gasto.get('cantidad', 0))
            gastos_data.append([fecha, desc, cat, f"${monto:.2f}"])
        
        gastos_table = Table(gastos_data, colWidths=[1.2*inch, 2*inch, 1.3*inch, 1.5*inch])
        gastos_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#004481')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
        ]))
        
        elements.append(gastos_table)
        elements.append(Spacer(1, 0.3*inch))
    
    # Ahorros
    if 'ahorros' in datos and datos['ahorros']:
        elements.append(Paragraph("DETALLE DE AHORROS", heading_style))
        ahorros_data = [['Fecha', 'Descripción', 'Monto']]
        for ahorro in datos['ahorros'][:20]:
            fecha = str(ahorro['fecha']) if 'fecha' in ahorro else ''
            desc = ahorro.get('descripcion', 'Ahorro')[:50]
            monto = float(ahorro.get('cantidad', 0))
            ahorros_data.append([fecha, desc, f"${monto:.2f}"])
        
        ahorros_table = Table(ahorros_data, colWidths=[1.5*inch, 3.5*inch, 2*inch])
        ahorros_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f7f0')])
        ]))
        
        elements.append(ahorros_table)
        elements.append(Spacer(1, 0.3*inch))
    
    # Métricas adicionales
    if 'racha_ahorro' in datos:
        elements.append(Paragraph("MÉTRICAS ADICIONALES", heading_style))
        metricas_data = [
            ['Racha de Ahorro', f"{datos['racha_ahorro']} días"],
            ['Total Ahorros Acumulados', f"${datos.get('total_ahorros', 0):.2f}"]
        ]
        
        if 'total_gastos_lifetime' in datos:
            metricas_data.append(['Total Gastos (Histórico)', f"{datos['total_gastos_lifetime']} transacciones"])
        
        metricas_table = Table(metricas_data, colWidths=[3.5*inch, 2.5*inch])
        metricas_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e0e0e0')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        elements.append(metricas_table)
    
    # Pie de página
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("FinanIA - Sistema de Gestión Financiera Personal", footer_style))
    elements.append(Paragraph(f"Generado el {fecha_consulta}", footer_style))
    
    # Construir PDF
    doc.build(elements)
    return output_path

def generar_reporte_semanal_global_pdf(datos_globales, usuarios_datos, output_path):
    """Generar reporte PDF semanal global para administrador"""
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#004481'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#004481'),
        spaceAfter=12
    )
    
    # Título
    elements.append(Paragraph("REPORTE SEMANAL GLOBAL", title_style))
    elements.append(Paragraph(f"Período: {datos_globales.get('fecha_inicio', '')} - {datos_globales.get('fecha_fin', '')}", 
                             styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Estadísticas Globales
    elements.append(Paragraph("ESTADÍSTICAS GLOBALES", heading_style))
    
    stats_data = [
        ['Métrica', 'Valor'],
        ['Total Usuarios', str(datos_globales.get('total_usuarios', 0))],
        ['Usuarios Activos', str(datos_globales.get('usuarios_activos', 0))],
        ['Gastos Totales', f"${datos_globales.get('total_gastos', 0):.2f}"],
        ['Ahorros Totales', f"${datos_globales.get('total_ahorros', 0):.2f}"],
        ['Gastos del Período', f"${datos_globales.get('gastos_periodo', 0):.2f}"],
        ['Ahorros del Período', f"${datos_globales.get('ahorros_periodo', 0):.2f}"]
    ]
    
    stats_table = Table(stats_data, colWidths=[3.5*inch, 2.5*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#004481')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Resumen por Usuario
    if usuarios_datos:
        elements.append(Paragraph("RESUMEN POR USUARIO", heading_style))
        
        usuarios_data = [['Usuario', 'Email', 'Gastos', 'Ahorros', 'Balance']]
        for usuario_data in usuarios_datos:
            usuario = usuario_data.get('usuario', {})
            usuarios_data.append([
                usuario.get('nombre', 'N/A'),
                usuario.get('email', 'N/A'),
                f"${usuario_data.get('total_gastos', 0):.2f}",
                f"${usuario_data.get('total_ahorros', 0):.2f}",
                f"${usuario_data.get('balance', 0):.2f}"
            ])
        
        usuarios_table = Table(usuarios_data, colWidths=[1.5*inch, 2*inch, 1*inch, 1*inch, 1*inch])
        usuarios_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ffd100')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
        ]))
        
        elements.append(usuarios_table)
    
    # Pie de página
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    fecha = datetime.now().strftime('%d/%m/%Y %H:%M')
    elements.append(Paragraph("FinanIA - Reporte Administrativo", footer_style))
    elements.append(Paragraph(f"Generado el {fecha}", footer_style))
    
    doc.build(elements)
    return output_path

