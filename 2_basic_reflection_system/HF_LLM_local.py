from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace

llm = HuggingFacePipeline.from_model_id(
    model_id="Qwen/Qwen2.5-1.5B-Instruct",
    task="text-generation",
    device=-1,   # CPU
    pipeline_kwargs={
        "max_new_tokens": 50,
        "temperature": 0.3,
        "do_sample": False,
    }
)


chats = ChatHuggingFace(llm = llm)
results = chats.invoke("what do you knnow abnout the Gradient Descent in Machine Learning")

print(results.content)