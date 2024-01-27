import os

from flask import Flask, flash, redirect, render_template, request, session

# Configure application
app = Flask(__name__)