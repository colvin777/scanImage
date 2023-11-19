from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import base64
from langserve import add_routes, CustomUserType
from pirate_speak.chain import chain as pirate_speak_chain
from langchain.pydantic_v1 import Field
from langchain.schema.runnable import RunnableLambda
from constants.model_templates import vision_template
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, BaseMessage
import binascii
from langchain.document_loaders.blob_loaders import Blob
from langchain.document_loaders.parsers.pdf import PDFMinerParser

from controllers.uploadFile import upload
from controllers.scanImage import scamImageRoute

app = FastAPI()
app.include_router(upload)
app.include_router(scamImageRoute)
app.mount("/static", StaticFiles(directory="uploaded_images"), name="static")

llm = ChatOpenAI(model="gpt-4-vision-preview", temperature=0, max_tokens=1024)


class ImageProcessingRequest(CustomUserType):
    """Request including a base64 encoded image."""

    # The extra field is used to specify a widget for the playground UI.
    image: str = Field(..., extra={"widget": {"type": "base64file"}})
    num_chars: int = 1024


def _process_image(request: ImageProcessingRequest) -> BaseMessage:
    """Extract the text from the first page of the PDF."""
    sys = """
            - 角色：图像分析师
            - 特长：具备高级视觉能力，用于分析和解释视觉数据。专注于图像中的对象识别和分类。
        """

    # 读取文件内容
    content = base64.b64decode(request.image.encode("utf-8"))
    # 将内容转换为 base64
    encoded = binascii.b2a_base64(content, newline=False)
    base64_image = encoded.decode('utf-8')
    prompt = [
        AIMessage(content=sys),
        HumanMessage(content=[
            {"type": "text", "text": vision_template},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                },
            },
        ])
    ]
    result = llm.invoke(prompt)

    print(result)
    return result


# ATTENTION: Inherit from CustomUserType instead of BaseModel otherwise
#            the server will decode it into a dict instead of a pydantic model.
class FileProcessingRequest(CustomUserType):
    """Request including a base64 encoded file."""

    # The extra field is used to specify a widget for the playground UI.
    file: str = Field(..., extra={"widget": {"type": "base64file"}})
    num_chars: int = 1024


def _process_file(request: FileProcessingRequest) -> str:
    """Extract the text from the first page of the PDF."""
    content = base64.b64decode(request.file.encode("utf-8"))
    blob = Blob(data=content)
    documents = list(PDFMinerParser().lazy_parse(blob))
    content = documents[0].page_content
    return content[: request.num_chars]


add_routes(
    app,
    RunnableLambda(_process_file).with_types(input_type=FileProcessingRequest),
    config_keys=["configurable"],
    path="/pdf",
)

add_routes(
    app,
    RunnableLambda(_process_image).with_types(input_type=ImageProcessingRequest),
    config_keys=["configurable"],
    path="/scanImage",
)

# Edit this to add the chain you want to add

add_routes(app, pirate_speak_chain, path="/pirate-speak")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
