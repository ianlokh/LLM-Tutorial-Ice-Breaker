from flask import Flask, render_template, request, jsonify
from summarise_profile import summarise_person

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    person_info, profile_pic_url = summarise_person(name=name)

    summary_and_facts = {
        "summary": person_info.summary,
        "facts": person_info.facts
    }

    return jsonify(
        {
            "summary_and_facts": summary_and_facts,
            # "summary": person_info.summary,
            # "facts": person_info.facts,
            "interests": person_info.topics_of_interest,
            "ice_breakers": person_info.ice_breakers,
            "picture_url": profile_pic_url
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
# app = Flask(__name__)
#
#
# @app.route("/")
# def index():
#     return render_template("index.html")
#
#
# @app.route("/process", methods=["POST"])
# def process():
#     name = request.form["name"]
#     summary_and_facts, interests, ice_breakers, profile_pic_url = ice_break_with(
#         name=name
#     )
#     return jsonify(
#         {
#             "summary_and_facts": summary_and_facts.to_dict(),
#             "interests": interests.to_dict(),
#             "ice_breakers": ice_breakers.to_dict(),
#             "picture_url": profile_pic_url,
#         }
#     )
#
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", debug=True)
