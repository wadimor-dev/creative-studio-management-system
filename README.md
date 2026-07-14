# Creative Studio Management System (CSMS)

Creative Studio Management System (CSMS) is an internal web application developed to manage creative production workflows, inventory assets, product movement, reporting, and employee activities within the Creative Division.

The system is built using a modern client-server architecture with a React frontend and a FastAPI backend.

---

# Features

## Dashboard
- Real-time studio overview
- Current active workers
- KPI monitoring
- Analytics charts
- Activity summary

## Work Management
- Daily work activities
- Start / Pause / Resume / Complete workflow
- Working duration tracking
- Activity history

## Inventory Management
- Inventory Items
- Categories
- Locations
- Stock movement
- Borrow / Return assets
- Inventory transaction history

## Product Management
- Product Catalog
- Product Master Data
- Product Movements
- Stock Overview

## Reports
- Daily Report
- Weekly Report
- Monthly Report
- Export Excel
- Export PDF

## User Management
- User Administration
- Role Management
- Permission Based Access Control (PBAC)

---

# Technology Stack

Frontend

- React
- Vite
- TailwindCSS
- React Hook Form
- Axios
- React Router
- Lucide React

Backend

- FastAPI
- SQLAlchemy
- Pydantic
- MySQL
- JWT Authentication

---

# Architecture

```
Frontend (React)

        │

REST API

        │

Backend (FastAPI)

        │

Business Services

        │

Repositories

        │

MySQL Database
```

---

# Security

The system uses:

- JWT Authentication
- Permission Based Access Control (PBAC)
- Route Protection
- API Authorization
- Role Permission Mapping

---

# Project Structure

```
creative-studio-management-system/

backend/
frontend/

README.md
```

---

# Installation

See:

- backend/README.md
- frontend/README.md

---

# License

Internal Project

Creative Division

Wadimor
