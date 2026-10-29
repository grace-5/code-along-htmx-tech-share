import time
from markupsafe import escape
from flask import Flask, render_template, request
import htmx_tech_share.database as database

app = Flask(__name__)

limit = 4; 
@app.route('/')
def index():

    yap_html = ""
    for idx, text in yap_list.items():
        yap_html += yap_display(idx, text)

    return render_template("index.html", images=database.get_images(limit), limit=limit, yap_html=yap_html)

# We want to display this after clicking a button
@app.route('/clicked', methods=["GET"])
def clicky():
    time.sleep(0.5) #artificial delay to display load
    return f'<p style="color:crimson;">This message was generated dynamically with HTMX! Yippee!!</p>'

@app.route("/scroll/")
def scroll():
    time.sleep(1) #artificial delay to display load
    page = request.args.get("pages", 1, type = int)
    return render_template("scroll.html", page=page, images=database.get_images(limit), limit=limit)







#non-demo for extra examples
slop_list = [
    "That time I got reincarnated as a slime",
    "Solo Leveling",
    "The Eldest Son of Noble Martial Family Returns from Hell After 100 Years",
    "The Evergreen Records",
]

yap_list = {
    1: "yap",
    2: "yapyapyap"
}
next_id = 3

def yap_display(text_id, text):
    return (
        # escape() is a good security measure when rendering HTML in flask to prevent injection attacks. Not covered in tech share
        # read more in flask docs
        # https://flask.palletsprojects.com/en/stable/quickstart/#html-escaping
        f'<li class="fade">{escape(text)}'

        # hx-delete: Issues a DELETE request to the given URL
        # https://htmx.org/docs/#triggers
        f'<button hx-delete="/yaplist/{text_id}"'

        # closest <CSS selector> = Tells htmx to swap AJAX response to nearest matching ancestor
        # in this case, the li when the button inside it is clicked
        # https://htmx.org/attributes/hx-target/
        f'hx-target="closest li" hx-swap="outerHTML swap:500ms"'

        # https://htmx.org/docs/#confirming self explanatory I think
        f'hx-confirm="You sure you wanna delete this?">DELETE</button></li>'
    )

@app.route('/search', methods=["GET"])
def search():
    slop = request.args.get("slop","").strip().lower()

    matches = []

    for s in slop_list:
        if slop in s.lower():
            matches.append(s)

    if not matches:
        return "<li>You haven't consumed enough slop yet, poser. (No matches)</li>"

    # note that escape() is used here
    return "".join(f"<li>{escape(s)}</li>" for s in matches)


@app.route('/yaplist', methods=["GET", "POST"])
def add_yap():
    global next_id
    text = request.form.get("text","").strip()
    if not text:
        return ""

    text_id = next_id
    next_id += 1
    yap_list[text_id] = text
    return yap_display(text_id, text)

@app.route('/yaplist/<int:text_id>', methods=["DELETE"])
def delete_yap(text_id):
    yap_list.pop(text_id)
    return ""


if __name__ == '__main__':
    app.run(debug=True, port=5001)

