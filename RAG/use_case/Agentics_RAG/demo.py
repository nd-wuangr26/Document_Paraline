from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


# -------------------
# 1. Định nghĩa router
# -------------------
def router(state):
    last_message = state["messages"][-1]["content"].lower()
    if "thời tiết" in last_message or "weather" in last_message:
        return "weather"
    else:
        return "wikipedia"


# -------------------
# 2. Khởi tạo tool nodes
# -------------------
# Weather → dùng DuckDuckGo search để giả lập
weather_tool = DuckDuckGoSearchRun()
weather_node = ToolNode([weather_tool])

# Wikipedia
wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
wiki_node = ToolNode([wiki_tool])


# -------------------
# 3. Tạo graph
# -------------------
graph = StateGraph(dict)

# Add nodes
graph.add_node("router", router)
graph.add_node("weather", weather_node)
graph.add_node("wikipedia", wiki_node)

# Entry point
graph.set_entry_point("router")

# Route từ router tới 2 nhánh
graph.add_conditional_edges(
    "router",
    router,
    {"weather": "weather", "wikipedia": "wikipedia"},
)

# Kết thúc
graph.add_edge("weather", END)
graph.add_edge("wikipedia", END)

# Compile
app = graph.compile()


# -------------------
# 4. Test
# -------------------
if __name__ == "__main__":
    query1 = "Hôm nay thời tiết ở Hà Nội thế nào?"
    result1 = app.invoke({
        "messages": [{"role": "user", "content": query1}]
    })
    print("Weather Result:", result1)

    query2 = "Ai là người phát minh ra điện thoại?"
    result2 = app.invoke({
        "messages": [{"role": "user", "content": query2}]
    })
    print("Wikipedia Result:", result2)
