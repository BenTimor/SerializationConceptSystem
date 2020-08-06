from flask import Flask, render_template, request, make_response, redirect, url_for

from blog import Config, User, Comment, Post

app = Flask(__name__)

def login_or_register():
    # If the request method is 'Get' it means that we're just requesting the page and not sending any form
    if request.method == "POST":
        username = request.values.get("inputtext1")
        password = request.values.get("inputtext2")
        user = User.get_user(username)

        # If user is None, it means it doesn't exist and we have to create it.
        if not user:
            User.new_user(username, password, False)
            user = User.get_user(username)

        if user.password == password:
            # Converting the template into a response
            resp = make_response(render_template("index.html", config=Config.config, user=user))
            # Setting the cookies
            resp.set_cookie("username", username)
            resp.set_cookie("password", password)
            return resp, user

def login_cookies():
    user = User.get_user(request.cookies.get("username"))
    password = request.cookies.get("password")
    # If the user exist and if it equals to the password, return
    if user and user.password == password:
        return render_template("index.html", config=Config.config, user=user), user

@app.route("/", methods=["POST", "GET"])
def index():
    # Try login, try cookies, else return template
    resp = login_or_register() or login_cookies()
    if resp:
        resp, user = resp
        # If there is a comment, create a new one
        comment_content = request.values.get("comment")
        if comment_content:
            Comment.new_comment(int(request.values.get("post-id")), user.name, comment_content)

        return resp

    return render_template("index.html", config=Config.config)

@app.route("/admin", methods=["POST", "GET"])
def admin():
    resp = login_cookies()
    if resp and request.method == "POST":
        title = request.values.get("title")
        content = request.values.get("content")
        Post.new_post(resp[1].name, title, content)
        return redirect(url_for("index"))

    return render_template("admin.html", user=(resp[1] if resp else None))

if __name__ == "__main__":
    Config.setup()
    app.run(debug=True)