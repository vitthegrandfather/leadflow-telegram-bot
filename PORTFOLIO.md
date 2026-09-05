# Telegram Lead Management Bot with CRM Workflow

**Project type:** Personal demonstration project

## Overview

LeadFlow Bot collects structured service requests in Telegram and gives an
administrator a compact CRM workflow for reviewing, updating, and exporting
leads.

## Business problem

Service businesses often receive incomplete enquiries across multiple chats.
Important details are missing, requests are difficult to track, and manual
copying into spreadsheets wastes time.

## Solution

The bot guides a customer through a validated multi-step brief, stores the
request, assigns a readable lead number, and immediately notifies authorized
administrators. Administrators can review requests, update their status, add
internal notes, inspect counts, and export the data to CSV.

## Key functionality

- Structured customer intake with confirmation, editing, and cancellation
- Five service categories and four preferred contact methods
- Personal request history for customers
- Admin-only lead desk with pagination and status management
- Customer notifications after status changes
- Internal administrator notes
- UTF-8 CSV export
- Duplicate-submission protection
- Database migrations and fictional seed data
- Automated service, repository, validation, security, and customer-flow tests

## Technology stack

Python 3.12, aiogram 3, SQLAlchemy 2, SQLite, Alembic, Pydantic Settings,
pytest, pytest-asyncio, Ruff, Docker, and Docker Compose.

## Upwork description

LeadFlow Bot is a personal demonstration project showing a complete Telegram
lead-intake workflow for a service business. Customers submit a structured
brief through a validated multi-step form, review their information, and
receive a readable request number. Authorized administrators receive new-lead
notifications, browse requests, update statuses, add internal notes, view
operational counts, and export the database to CSV. The application uses a
modular architecture with thin Telegram handlers, a service layer for business
rules, repositories for database access, Alembic migrations, structured
logging, environment-based configuration, Docker support, and automated tests.
All names and contact details shown in the demonstration are fictional.

## Recommended Upwork skills

Python, Telegram Bot, aiogram, SQLAlchemy, SQLite, API Integration, Automation,
Chatbot Development, Docker, Git, and Backend Development.
