from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain
)


def run_research_pipeline(topic: str) -> dict:

    state = {}

    # ==============================
    # STEP 1 - SEARCH AGENT
    # ==============================

    print("\n" + "=" * 50)
    print("Step 1 - Search agent is working...")
    print("=" * 50)

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            ("user", f"Find recent, reliable, and detailed information about: {topic}")
        ]
    })

    state["search_results"] = search_result["messages"][-1].content

    print("\nSearch results:\n", state["search_results"])


    # ==============================
    # STEP 2 - READER AGENT
    # ==============================

    print("\n" + "=" * 50)
    print("Step 2 - Reader agent is scraping top resources...")
    print("=" * 50)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URLs and scrape them for deeper content.\n\n"
                f"Search results:\n{state['search_results'][:8000]}"
            )
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nScraped content:\n", state["scraped_content"])


    # ==============================
    # STEP 3 - WRITER CHAIN
    # ==============================

    print("\n" + "=" * 50)
    print("Step 3 - Writer is drafting the report...")
    print("=" * 50)

    research_combined = (
        f"Search results:\n{state['search_results']}\n\n"
        f"Detailed scraped content:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\nFinal report:\n", state["report"])


    # ==============================
    # STEP 4 - CRITIC CHAIN
    # ==============================

    print("\n" + "=" * 50)
    print("Step 4 - Critic is reviewing the report...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\nCritic feedback:\n", state["feedback"])


    # ==============================
    # RETURN FINAL STATE
    # ==============================

    return state


if __name__ == "__main__":

    topic = input("\nEnter a research topic: ")

    result = run_research_pipeline(topic)