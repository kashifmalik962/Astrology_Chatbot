from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

template = """
                Answer the question below:
                
                Here is the conversational history: {history}
                
                Question: {question}
                
                Answer: 
            """
print("model running...")
model = OllamaLLM(model="llama3.2:latest", temperature=0.1, top_k=10, top_p=0.8)
prompt = ChatPromptTemplate.from_template(template)
memory = ConversationBufferMemory(input_key="question", memory_key="history")
chain = LLMChain(llm=model, prompt=prompt, memory=memory)

# Clear or initialize the memory before new input
memory.clear()  # Clear any previous memory

# Now, start the conversation fresh with the current question
response = chain.invoke({"question": "what is the capital bird of india"})
result = response["text"]
print(result)
