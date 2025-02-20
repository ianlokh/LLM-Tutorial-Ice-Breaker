from typing import Tuple

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent

from output_parsers import (
    person_intel_parser,
    PersonIntel
)

from json_repair import repair_json

# information = """ Elon Reeve Musk (/ˈiːlɒn/ EE-lon; born June 28, 1971) is a business magnate and investor. He is
# the founder, CEO and chief engineer of SpaceX; angel investor, CEO and product architect of Tesla, Inc.; founder,
# owner, CTO and chairman of X Corp. and Twitter; founder of the Boring Company; co-founder of Neuralink and OpenAI;
# and president of the philanthropic Musk Foundation. Musk is the wealthiest person in the world, with an estimated
# net worth as of July 6, 2023, of around US$248 billion according to the Bloomberg Billionaires Index and $251.1
# billion according to Forbes's Real Time Billionaires list, primarily from his ownership stakes in Tesla and
# SpaceX.[4][5][6] Musk was born in Pretoria, South Africa, and briefly attended the University of Pretoria before
# moving to Canada at age 18, acquiring citizenship through his Canadian-born mother. Two years later,
# he matriculated at Queen's University and transferred to the University of Pennsylvania, where he received
# bachelor's degrees in economics and physics. He moved to California in 1995 to attend Stanford University. After
# two days, he dropped out and, with his brother Kimbal, co-founded the online city guide software company Zip2. Zip2
# was acquired by Compaq for $307 million in 1999, and with $12 million of the money he made, that same year Musk
# co-founded X.com, a direct bank. X.com merged with Confinity in 2000 to form PayPal. In 2002, eBay acquired PayPal
# for $1.5 billion, and that same year, with $100 million of the money he made, Musk founded SpaceX, a spaceflight
# services company. In 2004, he was an early investor in the electric vehicle manufacturer Tesla Motors,
# Inc. (now Tesla, Inc.). He became its chairman and product architect, assuming the position of CEO in 2008. In
# 2006, he helped create SolarCity, a solar energy company that was acquired by Tesla in 2016 and became Tesla
# Energy. In 2013, Musk proposed a hyperloop high-speed vactrain transportation system. In 2015, he co-founded
# OpenAI, a nonprofit artificial intelligence research company. The following year, he co-founded Neuralink—a
# neurotechnology company developing brain–computer interfaces—and the Boring Company, a tunnel construction company.
# In 2022, his acquisition of Twitter for $44 billion was completed. Musk has expressed views that have made him a
# polarizing figure. He has been criticized for making unscientific and misleading statements, including that of
# spreading COVID-19 misinformation. In 2018, the U.S. Securities and Exchange Commission (SEC) sued Musk for falsely
# tweeting that he had secured funding for a private takeover of Tesla. To settle the case, Musk stepped down as
# chairman of Tesla and paid a $20 million fine. """

name = "Ian Lo"


def summarise_person(name: str) -> Tuple[PersonIntel, str]:
    # linkedin_profile_url = linkedin_lookup_agent(name=name)
    # linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)
    linkedin_data = scrape_linkedin_profile("https://gist.githubusercontent.com/ianlokh"
                                            "/723a9ca7380920fd7dae9ffd3cd9b2de/raw/ab87f07908e68f52d6faabb6cc94996a509aaa88/my_linkedin_profile_v2.json")

    # twitter_username = twitter_lookup_agent(name=name)
    # tweets = scrape_user_tweets(username=twitter_username, num_tweets=100)
    tweets = ""

    summary_template = """
        given the LinkedIn information {linkedin_information} and Twitter information {twitter_information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
        3. a topic that may interest them
        4. 2 creative ice-breakers to open up a conversation with them
        \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(input_variables=["linkedin_information", "twitter_information"],
                                             template=summary_template,
                                             partial_variables={
                                                 "format_instructions": person_intel_parser.get_format_instructions()}
                                             )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    result = chain.run(linkedin_information=linkedin_data, twitter_information=tweets)
    result = repair_json(result)
    print(result)
    return person_intel_parser.parse(result), linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    print("Hello LangChain")
    result = summarise_person(name=name)
