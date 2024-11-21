from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader
import io


def add_image_to_existing_pdf(pdf_path, image_path, output_pdf_path, page_number, x_position, y_position, width, height):
    """
    在已有PDF文件的指定页面的特定位置覆盖添加PNG图片，并导出新的PDF文件。

    参数:
    pdf_path (str): 原始PDF文件的路径。
    image_path (str): 要添加的PNG图片的路径。
    output_pdf_path (str): 输出的包含添加图片后的新PDF文件的路径。
    page_number (int): 要添加图片的页码（从0开始计数）。
    x_position (int): 图片在页面上的横坐标位置（以页面左上角为原点，单位根据页面尺寸设定）。
    y_position (int): 图片在页面上的纵坐标位置（以页面左上角为原点，单位根据页面尺寸设定）。
    width (int): 图片添加到页面上呈现的宽度（单位根据页面尺寸设定，可根据需求调整比例缩放图片）。
    height (int): 图片添加到页面上呈现的高度（单位根据页面尺寸设定，可根据需求调整比例缩放图片）。
    """
    # 第一步：读取原始PDF文件
    reader = PdfReader(open(pdf_path, "rb"))
    writer = PdfWriter()
    total_pages = len(reader.pages)

    # 检查指定页码是否在有效范围内
    if page_number < 0 or page_number >= total_pages:
        raise ValueError("指定的页码超出了PDF文件的总页数范围")

    # 第二步：获取要添加图片的目标页面并获取页面尺寸信息
    target_page = reader.pages[page_number]
    page_width = target_page.mediabox.width
    page_height = target_page.mediabox.height

    # 第三步：将图片绘制到目标页面上
    packet = io.BytesIO()
    canvas_obj = io.BytesIO()
    img = ImageReader(image_path)
    img_width, img_height = img.getSize()
    # 根据传入的坐标和尺寸设置，在目标页面上绘制图片
    canvas = io.BytesIO()
    can = create_canvas(canvas, page_width, page_height)
    can.drawImage(img, x_position, y_position, width, height)
    can.save()
    canvas_obj.write(canvas.getvalue())
    canvas_obj.seek(0)

    # 将绘制图片后的内容覆盖到目标页面上
    img_page = PdfReader(canvas_obj).pages[0]
    target_page.merge_page(img_page)

    # 第四步：将处理后的页面添加到输出的PDF对象中
    writer.add_page(target_page)
    for page in reader.pages:
        if page!= target_page:
            writer.add_page(page)

    # 第五步：将合并后的内容写入最终的PDF文件
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)


def create_canvas(canvas, width, height):
    """
    创建一个用于在指定尺寸页面上绘图的canvas对象。
    """
    canvas = canvas or io.BytesIO()
    from reportlab.pdfgen import canvas as rl_canvas
    return rl_canvas.Canvas(canvas, pagesize=(width, height))

# pdf_path = "../Data/YZY.pdf"
# image_path = "../Data/image.png"
# output_pdf_path = "output.pdf"
# page_number = 0  # 这里表示在第1页（页码从0开始计数）添加图片
# x_position = 300  # 图片横坐标位置，可根据实际需求调整
# y_position = 100  # 图片纵坐标位置，可根据实际需求调整
# width = 200  # 图片在页面上呈现的宽度，可按需缩放
# height = 150  # 图片在页面上呈现的高度，可按需缩放
# add_image_to_existing_pdf(pdf_path, image_path, output_pdf_path, page_number, x_position, y_position, width, height)
