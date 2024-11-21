import os
import re
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import Data.text as text
import Model.my_datetime as my_date
import Model.save_pdf as save_pdf

# pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ opencv-contrib-python
# streamlit run manage.py
# pip freeze > requirements.txt

# 设置页面标题
st.title("邢台总医院预住院系统")
# st.subheader("预住院患者知情同意书")

long_text = text.text
st.markdown(f'<div style="height:300px;overflow-y:scroll;">{long_text}</div>', unsafe_allow_html=True)
name = st.text_input("请输入患者姓名：")
st.write(f'请患者{name}或家属签字：')


# 创建一个可绘制的画布
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # 填充颜色
    stroke_width=5,  # 笔触宽度
    stroke_color="#000000",  # 笔触颜色
    background_color="#FFFFF0",  # 背景颜色
    update_streamlit=True,  # 实时更新
    height=400,  # 画布高度
    drawing_mode="freedraw",  # 绘图模式
    key="canvas",  # 画布的唯一标识
)

upload_button = st.button('点击上传签字')
image = canvas_result.image_data
pattern = r'^[\u4e00-\u9fa5]{2,4}$'

# 显示绘图结果
if upload_button:
    if re.match(pattern, name) and image is not None:

        # 获取当前日期
        today = my_date.my_date()
        folder_path = "ImageData/" + today
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, name + ".png")
        file_path1 = os.path.join(folder_path, name + ".pdf")

        if os.path.exists(file_path):
            st.warning("文件已存在，是否覆盖？")
            if st.button("覆盖"):
                # 在这里添加覆盖文件的代码，例如：
                st.success('您已成功上传签字文件')
                st.success("文件已覆盖")
            elif st.button("取消"):
                st.info("已取消覆盖操作")
        else:
            # 将图像数据转换为Image对象（Pillow库中的图像对象）
            image = Image.fromarray(image)
            # 保存图像为png文件
            image.save(file_path)
            if file_path1 is not None:
                save_pdf.add_image_to_existing_pdf('./Data/YZY.pdf', file_path, file_path1, 0, 300, 100, 200, 150)
                st.success('您已成功上传签字文件')
    else:st.warning('未能成功上传文件')
