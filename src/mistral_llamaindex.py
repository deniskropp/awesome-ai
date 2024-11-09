import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core import Settings

# Load data
reader = SimpleDirectoryReader(input_dir='./Qwick/prompt')
documents = reader.load_data()

# Define LLM and embedding model
llm = MistralAI(api_key=os.environ["MISTRAL_API_KEY"], model="mistral-medium")
embed_model = MistralAIEmbedding(model_name="mistral-embed", api_key=os.environ["MISTRAL_API_KEY"])
Settings.llm = llm
Settings.embed_model = embed_model
# Create vector store index
index = VectorStoreIndex.from_documents(documents)

# Create query engine
query_engine = index.as_query_engine(similarity_top_k=2)
response = query_engine.query(
    "What were the two main things the author worked on before college?"
)
print(str(response))
