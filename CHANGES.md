# CHANGES.md

## Overview

This document outlines the critical issues identified in the original Flask-based user management API and the changes made to improve code quality, security, and maintainability.

---

## 🔍 Major Issues Identified

1. **SQL Injection Vulnerabilities**
   - Direct string interpolation was used in SQL queries.
   - This made the application highly vulnerable to SQL injection attacks.

2. **Poor Input Validation**
   - No validation of request data before using it in queries.
   - Missing checks for required fields or data types.

3. **Improper Use of HTTP Status Codes**
   - Routes returned plain strings and always used status 200, even for errors.

4. **Tight Coupling Between Logic and Routes**
   - All database and business logic were embedded directly in route handlers.
   - No separation of concerns or reusability.

5. **Unsafe Error Reporting**
   - Some debug `print()` statements were left in production logic.
   - No consistent error handling or logging.

6. **Lack of JSON API Consistency**
   - Most endpoints returned stringified raw data (e.g., tuple dumps from SQLite), not structured JSON.

---

## ✅ Changes Made

### 🔒 Security

- Replaced all raw SQL string interpolation with **parameterized queries** using `?` placeholders.
- Validated and sanitized all incoming user data (e.g., required fields, types, string length).
- Removed any debug prints or sensitive logs from the production code.

### 🧱 Code Structure

- Refactored the route handlers to be clean and concise.
- Moved reusable logic like database access into helper functions.
- Used meaningful function and variable names throughout.

### 🔁 Error Handling & Status Codes

- Implemented try-except blocks for all database operations.
- Returned proper HTTP status codes (`200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`, `500 Internal Server Error`) based on operation results.
- Standardized all responses using JSON (no raw strings returned).

### 🔍 Data Output Consistency

- All routes now return JSON objects, not stringified tuples.
- Uniform success/error message formats across endpoints.

---

## 🤔 Assumptions and Trade-offs

- Kept the SQLite database and file structure as-is for simplicity.
- Did not add password hashing due to limited scope and instruction not to add new features.
- Skipped introducing Flask extensions (e.g., Marshmallow, SQLAlchemy) to avoid over-engineering.

---

## 📈 What Would Be Done With More Time

- Add **password hashing and salting** for secure login handling.
- Use **Flask Blueprints** for better modularity.
- Introduce **schema validation** using libraries like `pydantic` or `marshmallow`.
- Implement **structured logging** and metrics for better observability.
- Add **unit and integration tests** for all endpoints.
- Replace SQLite with a production-grade database like PostgreSQL.

---

## ✅ Final Result

- Application still runs with:  
  ```bash
  python app.py
