from google.adk.agents import Agent, SequentialAgent, ParallelAgent
from google.adk.tools import AgentTool, google_search
from google.adk.tools.function_tool import FunctionTool
from app.tools import get_amazon_deals_by_product, \
      get_alibaba_deals_by_product, ask_confirmation
from app.utils import google_model, llm_model

def build_amazon_agent():
    amazon = Agent(name="amazon_agent",
                   model=google_model,
                   tools=[get_amazon_deals_by_product],
                   description="Agent looks for the best Christmas gift deals over Amazon marketplace",
                   instruction="You are getting the name of product to look for into Amazon as a Christmas gift." \
                   "Collect the best ten deals and provide back the list of products with product_title, product_price," \
                   "product_original_price, product_star_rating, product_url, prdouct_photo." \
                   "Use the tool get_amazon_deals_by_product for performing the search and" \
                   "if you recieve max_price or sort_by use them to in the request.",
                   output_key="amazon")
    return amazon

def build_alibaba_agent():
    alibaba = Agent(name="AlibabaAgent",
                   model=google_model,
                   tools=[get_alibaba_deals_by_product],
                   description="Agent looks for the best Christmas gift deals over Alibaba marketplace",
                   instruction="You are getting the name of product to look for into Alibaba as a Christmas gift." \
                   "Collect the best ten deals and provide back the list of products available" \
                   "into field resultList. For each product collect title, itemUrl, image. " \
                   "The price is inside sku.def together with promotionPrice."  \
                   "All information about product must be provided back as " \
                   "product_original_price, product_star_rating, product_url, prdouct_photo." \
                   "Use the tool get_alibaba_deals_by_product for performing the search and" \
                   "if you recieve max_price use it in the request.",
                   output_key="alibaba")
    return alibaba

def build_root_agent(agents: dict[str, Agent], output_key: str):
    workflow = SequentialAgent(
       name="DirectorAgent",
       sub_agents=agents.values(),
       description="Coordinates the worflow among specialized agents to find the best Christmas gift deals"
    )
    output_field="{"+output_key+"}"
    json_format="""{ gifts: [ { name: sample1, description: sample_description, original_price: 10, current_price: 5, 
      marketplace: Amazon, rating: 5, order_url:https://amazon.com/sample, image_url:https://amazon.com/sample.png}]}"""
    elf_agent = Agent(
        name="ElfAgent",
        model=llm_model,
        tools=[AgentTool(workflow)],
        description="""ElfAgent is an expert Christmas gift advisor that finds the best deals on the web for 
         Christmas gifts, whether for a specific product or a category of products""",
        instruction=f"""You are a helpful Christmas Elf expert in finding the best gift deals online for the holiday season.
            Your task is to help users identify and summarize the top Christmas gift deals available across multiple marketplaces.
            Use the DirectorAgent to coordinate the activities for searching the best
            gift deals over different marketplaces.
            The list of best deals will be available in {output_key}. 
            Select only the top 10 deals based on the user needs and sort them by the best
            relationship between quality and price, keeping in mind they are intended as Christmas gifts.
            Provide the results as json document such as: {json_format} """
    )
    return elf_agent

def build_markeplace_agent(agents: list[Agent], input_key: str):
    input_field ="{"+input_key+"}"
    marketplaceSearchTeam = ParallelAgent(
        name="MarketplaceSearchTeam",
        description="""A team of agents that perform searches over
          different online marketplaces""",
        sub_agents=agents
    )
    aggregator_agent = Agent(
        name="ProductAggregatorAgent",
        model=llm_model,
        instruction="""Collect the list of Christmas gift products from the different marketplaces agents
        and combine them into a single list removing duplicates, sort them by the best 
        discount available and gift suitability. Each deal must contain product_title, product_description, product_original_price,
           product_price, product_star_rating, product_url, product_image, marketplace_source
        Provide back the final list of products as json file:
        {
          "products": [
            {
              "product_title": "...",
              "product_description": "...",
              "product_original_price": "...",
              "product_price": "...",
              "product_star_rating": "...",
              "product_url": "...",
              "product_image": "...",
              "marketplace_source": "Amazon | Alibaba"
            }
          ]
        }"""
    )
    maketplaceCoordinator = SequentialAgent(
        name="MarketplaceCoordinator",
        sub_agents=[marketplaceSearchTeam, aggregator_agent],
        description="An agent coordinator that looks for the best Christmas gift deals over multiple marketplaces"
    )

    marketplaceAgent = Agent(
        name="MarketplaceAgent",
        model=llm_model,
        tools=[AgentTool(maketplaceCoordinator)],
        description="Agent that looks for the best Christmas gift deals for a specific product or a category of products",
        instruction=f"""You are an expert in finding the best Christmas gift deals online for a specific product or a 
          category of products. Collect the list of products available in the field query of {input_field}.
          According to the amount of products, use the MarketplaceSearchTeam to find the best gift deals over
          multiple maketplaces in two different ways:
            1. If there is only a single product, use the product_name to find the best deals available 
            for that product as a Christmas gift.
            2. If there are multiple products, use a list of product_name to find the
            find only the best products suitable as Christmas gifts.
        Provide back to the user only the top 20 deals based on the best relationship between quality and discount""",
        output_key="deals"
    )
    return marketplaceAgent


def build_verification_agent(input_key):
   input_field ="{"+input_key+"}"
   print(f"VerifierAgent Input in {input_field}")
   verifier_agent = Agent(
      name="VerificationAgent",
      model=llm_model,
      instruction=f"""Collect the products in {input_field} and use the ask_confirmation tool to show them
      to the user and ask for his approval. Provide back the products if the user approved otherwise
      stop the conversation.""",
      output_key="verified_query",
      tools=[FunctionTool(func=ask_confirmation)]
   )
   return verifier_agent 

def google_agent():
    google = Agent(name="ProductSearchAgent",
                   model=google_model,
                   tools=[google_search],
                   description="An agent that collects information about Christmas gift ideas for a specific product"
                   "or a category of products.",
                   instruction="""You are an agent specialized in collecting and summarizing information about
                   the main features of a specific product or a category of products suitable as Christmas gifts." 
                   Determine from user's query if they are looking for a specific product or a category of products as gifts. 
                   Use the google_search tool for gathering data online about the product features, prices, and gift suitability. 
                   Make a list of the top 5 features providing their pros and cons and the cost of the product 
                   on the market. Collect these information in a json format like this: 
                   { 
                     "features": [
                     {
                       "feature_name": "...",
                       "feature_value": "...",
                       "pros": ["...", "..."],
                       "cons": ["...", "..."]
                     }],
                     "price": "...",
                     "product_name": "...",
                    }
                    Use this for each product if the target is a category of products""",
                   output_key="google_results")
    return google

search_agent = google_agent()
amazon_agent = build_amazon_agent()
alibaba_agent = build_alibaba_agent()
#verifier_agent = build_verification_agent(search_agent.output_key)
ecommerce_agents = [amazon_agent, alibaba_agent]
marketplace_agent = build_markeplace_agent(ecommerce_agents, search_agent.output_key)
agents = [search_agent, marketplace_agent]
root_agent = build_root_agent(agents={agent.name: agent for agent in agents}, output_key=marketplace_agent.output_key)
#root_agent = search_agent
