# CSMS Frontend

Frontend application for Creative Studio Management System.

---

# Technology

- React
- Vite
- TailwindCSS
- Axios
- React Router
- React Hook Form
- Lucide React

---

# Installation

Install dependencies

```bash
npm install
```

Run development

```bash
npm run dev
```

Production build

```bash
npm run build
```

Preview

```bash
npm run preview
```

---

# Environment

Create

```
.env
```

Example

```env
VITE_API_URL=http://localhost:8000/api/v1
```

---

# Folder Structure

```
src/

api/
assets/
components/
contexts/
hooks/
layouts/
pages/
routes/
utils/
```

---

# Authentication

Authentication uses JWT.

User information is stored inside

```
AuthContext
```

Protected routes require authentication before rendering.

---

# Permission System

Frontend also implements Permission Based Access Control.

Menu rendering

```
Sidebar
```

Route protection

```
ProtectedRoute
```

Feature visibility

```
hasPermission(user, Permission)
```

---

# API Layer

Axios

↓

Services

↓

Hooks

↓

Pages

---

# Main Pages

Dashboard

Work

Inventory

Products

Reports

Users

Profile

---

# Coding Standard

Pages

Only render UI.

Hooks

Handle data fetching.

Services

Handle API communication.

Components

Reusable UI only.
