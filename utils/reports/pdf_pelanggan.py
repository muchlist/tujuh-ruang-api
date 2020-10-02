import datetime

import os.path as ospath
from config import config
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader


def generate_pdf(pdf_name: str, data_pelanggan: list):

    # A4 = (210*mm,297*mm)
    path = config.get('temp_pdf_path')
    doc = SimpleDocTemplate(f'{path}{pdf_name}',
                            pagesize=A4,
                            rightMargin=72,
                            leftmargin=72,
                            topMargin=5,
                            bottomMargin=5)
    story = []

    """
    ------------------------------------------------------------------------
    HEADER
    """
    data = [
        ["GLOBAL PRINT"],
        ["Jl. Sutoyo S. Banjarmasin\nKalimantan Selatan"],
    ]

    # (SPAN, (begincol, beginrow), (endcol, endrow))
    tblstyle = TableStyle([
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 16),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ])

    tbl = Table(data, colWidths=[190*mm,])
    tbl.setStyle(tblstyle)
    story.append(tbl)
    story.append(Spacer(0, 10))

    """
    -------------------------------------------------------------------------
    TITLE
    """

    data = [
        ["LAPORAN DATA PELANGGAN"],
    ]

    tblstyle = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ])

    tbl = Table(data, colWidths=[190*mm])
    tbl.setStyle(tblstyle)
    story.append(tbl)
    story.append(Spacer(0, 5))

    """
    -------------------------------------------------------------------------
    DATA PELANGGAN
    """
    data = [["ID Pelanggan", "Nama Pelanggan", "Email","Alamat", ]]

    for i in range(len(data_pelanggan)):

        data.append([para(data_pelanggan[i]["id_pelanggan"]),
                     para(data_pelanggan[i]["nama"]),
                     para(data_pelanggan[i]["email"]),
                     para(data_pelanggan[i]["alamat"]),])

    tblstyle = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 0), (-1, 0), [colors.lightblue]),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('VALIGN', (0, 1), (-1, -1), "TOP"),
    ])

    tbl = Table(data, colWidths=[25*mm, 50*mm,
                                 55*mm, 60*mm,])  # total 190
    tbl.setStyle(tblstyle)
    story.append(tbl)
    story.append(Spacer(0, 10))

    # BUILD THE PDF
    doc.build(story)


def para(text: str) -> Paragraph:
    """
    Menginputkan text dan mengembalikan paragraph normal
    """
    normal_style = getSampleStyleSheet()["Normal"]
    return Paragraph(text, normal_style)
