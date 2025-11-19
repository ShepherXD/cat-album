import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from google.genai import types
load_dotenv()

# print(os.environ.get("NEKO"))dock
# image_path = input("请输入图片文件路径：")

def cat_recognize(): #！！要传入接收到的图片（64编码？
    image_path="/app/cat-img/shiro.jpg"

    with open(image_path, "rb") as f:
        image_data = f.read()


    prompt= '''
    你是一个猫专家，能通过猫的样子识别出猫的种类。你的工作是通过用户上传的猫照片用日语回答图中的猫是什么品种。如果你无法十分确定答案，则回答一个你认为最有可能的品种。
    你应当结构化输出：<breed>猫的品种</breed>
    举例：<breed>黒猫</breed>
    '''
    client=genai.Client()
    try:
        response=client.models.generate_content(
            model="gemini-2.5-flash", 
            config=types.GenerateContentConfig(
                system_instruction=prompt
            ),
            contents=[
                types.Part.from_bytes(
                    data=image_data,
                    mime_type='image/jpeg'
                )
            ]
        )

        result=response.text
        pattern=r"<breed>(.+)</breed>"
        breed=re.search(pattern,result).group(1)
        print(f" 猫的品种是： {breed} ")
        return breed
    except errors.ServerError as e:
        print(f"服务器拥挤:{str(e)}")
        return "服务器拥挤，请稍后再试"
    except errors.APIError as e:
        print(f"已达到API使用上限：{str(e)}")
        return "API用光啦，明天再来吧~"