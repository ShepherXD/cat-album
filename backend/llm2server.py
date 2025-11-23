import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from google.genai import types
load_dotenv()

# print(os.environ.get("NEKO"))dock
# image_path = input("请输入图片文件路径：")

def cat_recognize(image_data): #！！要传入接收到的图片（64编码？
    # image_path="/app/cat-img/shiro.jpg"


    prompt= '''
    You are a "Cat Expert AI" highly knowledgeable about all cat breeds and their characteristics worldwide. Your task is to observe user-uploaded cat photos and classify the cat accurately and clearly, strictly following the principles and format outlined below. You should always output structured data: <breed>Cat Breed</breed>.

    Example: <breed>Black Cat</breed>.

    There are two scenarios for determining the cat's breed/type.

    Scenario 1: Purebred Classification
    If the cat in the photo clearly exhibits the physical characteristics (face shape, bone structure, ears, coat, etc.) of a specific purebred cat recognized by international cat registries (such as CFA, TICA), use that as the classification standard.

    Examples: <breed>American Shorthair</breed>, <breed>British Shorthair</breed>, <breed>Japanese Bobtail</breed>...... and so on.

    Reference Link: 
    https://web.archive.org/web/20150111233321/http://www.cfainc.org/Breeds.aspx
    https://en.wikipedia.org/wiki/List_of_cat_breeds

    Scenario 2: Mixed/Domestic Cat Classification
    If the cat does not meet the criteria in Scenario 1, exhibits a mix of various breed characteristics, or possesses the common features of a Japanese domestic cat, the cat should be classified by the general term for its most prominent coat color or pattern.

    Examples (Japanese Terms): <breed>Kijitora</breed> (Brown Tabby), <breed>Chatora</breed> (Red/Orange Tabby), <breed>Mike Neko</breed> (Calico), <breed>Hachiware</breed> (Bi-color/Mask-and-Mantle), <breed>Kuro Neko</breed> (Black Cat)...... and so on.

    Additional Classification Principle
    1.For mixed-breed cats that resemble a purebred (e.g., a mixed-breed cat with the folded ears typical of a Scottish Fold), classify it as the recognized breed with the appended term "(Mixed Breed)".

    Example: <breed>Scottish Fold (Mixed Breed)</breed>

    2.If the photo appears to be an illustration or cartoon character and not a photograph of a real cat, classify it as how you recognized it.

    Example: <breed>Illust Cat</breed>, <breed>Cat girl(character)</breed>... and so on.
    '''
    client=genai.Client()
    try:
        response=client.models.generate_content(
            # model="gemini-2.5-flash", 
            model="gemini-2.5-pro",
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