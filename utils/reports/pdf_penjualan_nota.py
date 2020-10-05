from datetime import datetime, timedelta

from config import config
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from utils.rupiah_generator import rupiah_format


def generate_pdf(pdf_name: str, dp: dict):

    # A4 = (210*mm,297*mm)
    path = config.get('temp_pdf_path')
    doc = SimpleDocTemplate(f'{path}{pdf_name}',
                            pagesize=A4,
                            rightMargin=102,
                            leftmargin=102,
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
        ["============================================================="],
    ]

    # (SPAN, (begincol, beginrow), (endcol, endrow))
    tblstyle = TableStyle([
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 16),
        ('ALIGN', (0, 0), (-1, 1), 'CENTER')
    ])

    tbl = Table(data, colWidths=[130*mm, ])
    tbl.setStyle(tblstyle)
    story.append(tbl)
    story.append(Spacer(0, 10))

    """
    -------------------------------------------------------------------------
    TITLE
    """

    timenow = datetime.now()
    hours = 8
    hours_added = timedelta(hours = hours)

    timenow = timenow + hours_added

    data = [
        [f'Oleh : {dp.get("petugas")}'],
        [f'{timenow.strftime("%d/%m/%Y")}'],
        [f'Kepada Yth. {dp["pelanggan"]["nama_pelanggan"]}']
    ]

    tblstyle = TableStyle([
        ('ALIGN', (0, 1), (0, 1), 'RIGHT')
    ])

    tbl = Table(data, colWidths=[130*mm])
    tbl.setStyle(tblstyle)
    story.append(tbl)
    story.append(Spacer(0, 5))

    """
    -------------------------------------------------------------------------
    TITLE
    """

    satuan_bahan = "Unit"
    if "satuan_bahan" in dp["bahan"]:
        satuan_bahan = dp["bahan"]["satuan_bahan"]

    data = [
        ["KWITANSI"],
        ["============================================================="],
        [f'{dp["nama_pesanan"]}\n {dp["bahan"]["ukuran_x"]} x {dp["bahan"]["ukuran_x"]}            {dp["bahan"]["qty"]} {satuan_bahan}            @{dp["bahan"]["harga_bahan"]}'],
        ["============================================================="],
    ]

    tblstyle = TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'CENTER')
    ])

    tbl = Table(data, colWidths=[130*mm])
    tbl.setStyle(tblstyle)
    story.append(tbl)
    story.append(Spacer(0, 5))

    """
    -------------------------------------------------------------------------
    DATA PENJUALAN
    """
    data = [
        ["Total", rupiah_format(f'{dp["biaya"]["total_bayar"]}')],
        ["Uang Muka", rupiah_format(f'{dp["biaya"]["uang_muka"]}')],
        ["-----------------------------------------------------------------------------------------------------------", " "],
        ["Sisa", rupiah_format(f'{dp["biaya"]["sisa_bayar"]}')],
    ]

    if dp["biaya"]["apakah_lunas"]:
        data.insert(3, [f'Dibayar lunas pada {dp.get("diupdate").strftime("%d/%m/%Y")}', ""])

    tblstyle = TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('SPAN', (0, 2), (1, 2)),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
    ])

    tbl = Table(data, colWidths=[65*mm, 65*mm])  # total 190
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
