from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime



# Custom tool to save research output to a text file: To achieve this 1. Create a func that does what you want. 2. Wrap it in a Tool object
def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

save_tool = Tool(
     name="save_to_txt",
    func=save_to_txt,
    description="Save the research output to a text file."
)

#looking up wikipedia
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=750)

wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

#duckduckgo search
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information"
)

