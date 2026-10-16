
from SnackStack.rag import menu_vectorstore

query = "Show me vegan food with vegetables"

results = menu_vectorstore.similarity_search(
    query,
    k=3
)

print("\nCustomer query:", query)
print("\nRetrieved dishes:")

for doc in results:
    print("-" * 40)
    print(doc.page_content)
