import datetime

import os.path as ospath
from config import config
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from utils.rupiah_generator import rupiah_format


def generate_pdf(pdf_name: str, data_penjualan: list, start: str, end: str, title: str):

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

    tbl = Table(data, colWidths=[190*mm, ])
    tbl.setStyle(tblstyle)
    story.append(tbl)
    story.append(Spacer(0, 10))

    """
    -------------------------------------------------------------------------
    TITLE
    """

    data = [
        [title],
        [f'Periode {start.strftime("%d-%b-%Y")} sd {end.strftime("%d-%b-%Y")}']
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
    DATA PENJUALAN
    """
    data = [["Tanggal", "Nama Pelanggan", "Nama Pesanan",
             "Ukuran", "Qty", "Harga", "Jumlah"]]

    total = 0
    for i in range(len(data_penjualan)):

        total = total + data_penjualan[i]["biaya"]["total_bayar"]
        ukuran = f'{data_penjualan[i]["bahan"]["ukuran_x"]} x {data_penjualan[i]["bahan"]["ukuran_y"]}'
        date_string = str(data_penjualan[i]["dibuat"].strftime("%d-%m-%Y")).upper()

        data.append(
            [para(date_string),
             para(data_penjualan[i]["pelanggan"]["nama_pelanggan"]),
             para(data_penjualan[i]["nama_pesanan"]),
             para(ukuran),
             para(str(data_penjualan[i]["bahan"]["qty"])),
             rupiah_format(data_penjualan[i]["bahan"]["harga_bahan"],0,False),
             rupiah_format(data_penjualan[i]["biaya"]["total_bayar"],0,False)
             ]
        )

    data.append(["","","","","","TOTAL",rupiah_format(total)])

    tblstyle = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (5, 1), (6, -1), 'RIGHT'),
        ('SPAN', (0, -1), (4, -1),),
        ('ROWBACKGROUNDS', (0, 0), (-1, 0), [colors.lightblue]),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('VALIGN', (0, 1), (-1, -1), "TOP"),
    ])

    tbl = Table(data, colWidths=[25*mm, 40*mm,
                                 40*mm, 15*mm, 
                                 10*mm, 25*mm, 35*mm])  # total 190
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
