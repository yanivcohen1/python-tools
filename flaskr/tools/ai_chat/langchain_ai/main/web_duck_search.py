from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

res = search.invoke("Obama's first name?")

print(res)
