import uvicorn
from fastapi import FastAPI, Form
from main import client_request
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
new_cls = client_request()
origins = ["*"]

@app.post("/Paraphrasing/")
async def predict(text: str=Form(...)):
    with open('data.txt', 'r') as f:
        paraphrase_prompt = f.read()
    # paraphrase_prompt="Article: Searching a specific search tree for a binary key can be programmed recursively or iteratively.\nParaphrase: Searching a specific search tree according to a binary key can be recursively or iteratively programmed.\n\nArticle: It was first released as a knapweed biocontrol in the 1980s in Oregon , and it is currently established in the Pacific Northwest.\nParaphrase: It was first released as Knopweed Biocontrol in Oregon in the 1980s , and is currently established in the Pacific Northwest.\n\nArticle: 4-OHT binds to ER , the ER / tamoxifen complex recruits other proteins known as co-repressors and then binds to DNA to modulate gene expression.\nParaphrase: The ER / Tamoxifen complex binds other proteins known as co-repressors and then binds to DNA to modulate gene expression.\n\nArticle: In mathematical astronomy, his fame is due to the introduction of the astronomical globe, and his early contributions to understanding the movement of the planets.\nParaphrase: His fame is due in mathematical astronomy to the introduction of the astronomical globe and to his early contributions to the understanding of the movement of the planets. \n\n"
    text_changed = f'{paraphrase_prompt} Article: {text} \nParaphrase:'
    return new_cls.multi_function(text_changed)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# if __name__ == "__main__":
#     uvicorn.run(
#         "server:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True,
#         log_level="info",
#     )