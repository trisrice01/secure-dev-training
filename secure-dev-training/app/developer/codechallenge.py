from flask import Blueprint, request, render_template, redirect, flash, jsonify
from app.models.code_challenge import CodeChallenge
from app import db



def add_code_challenges():
    if CodeChallenge.query.count() == 0:
        challenges = [
            CodeChallenge(
                name="SQL Injection 101",
                flag="flag{example_sql_injection}",
                description="A basic SQL Injection challenge.",
                vuln_code="SELECT * FROM users WHERE username = 'admin' AND password = 'password'",
            ),
            CodeChallenge(
                name="Cross-Site Scripting",
                flag="flag{example_xss}",
                description="A simple Cross-Site Scripting vulnerability.",
                vuln_code="<script>alert('XSS')</script>",
            ),
            CodeChallenge(
                name="Buffer Overflow",
                flag="flag{example_buffer_overflow}",
                description="A challenge involving buffer overflow.",
                vuln_code="int main() { char buffer[10]; gets(buffer); }",
            ),
        ]
        db.session.add_all(challenges)
        db.session.commit()
