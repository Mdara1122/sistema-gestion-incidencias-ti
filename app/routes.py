from flask import Blueprint, render_template


main = Blueprint("main", __name__)


@main.get("/")
def inicio():
    return render_template("inicio.html")

