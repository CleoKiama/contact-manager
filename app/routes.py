from flask import render_template, flash, redirect, url_for
from app import app
from flask import Flask


@app.route("/message")
def home():
    return "<p>Hello there!!</p>"
