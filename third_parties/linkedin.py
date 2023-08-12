import os
import requests


def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    # note that the doc chain is important as LangChain will use the function description to decide when and how to
    # call this function or not for tasks

    # https://gist.githubusercontent.com/ianlokh/9536ca2fe0b9e4595cda80a6f884f43c/raw/014dfc610d913104ef8befe22c9afc3bf86aa7b2/my_linkedin_profile.json

    # api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    # header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}

    # response = requests.get(
    #     api_endpoint, params={"url": linkedin_profile_url}, headers=header_dic
    # )

    response = requests.get(
        "https://gist.githubusercontent.com/ianlokh/9536ca2fe0b9e4595cda80a6f884f43c/raw/014dfc610d913104ef8befe22c9afc3bf86aa7b2/my_linkedin_profile.json"
    )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None, "null")
        and k not in ["people_also_viewed", "certifications",
                      "similarly_named_profiles", "country",
                      "background_cover_image_url",
                      "experiences"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data
