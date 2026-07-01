import streamlit as st
from utils.auth import require_login
from utils.ui_theme import page_header

require_login()

page_header("Quiz Generator", "Generate quizzes from your uploaded notes.", "📝")