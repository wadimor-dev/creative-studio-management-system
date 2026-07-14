# Frontend Architecture

## 1. Overview
The CSMS Frontend is a Single Page Application (SPA) built with **React** and bundled using **Vite**. It provides a highly responsive, dynamic, and interactive user interface tailored for creative studio operations.

## 2. Technology Stack Deep-Dive
- **Framework:** React v19
- **Build Tool:** Vite (chosen for lightning-fast HMR and optimized builds)
- **CSS Framework:** TailwindCSS v4 (Utility-first styling approach)
- **HTTP Client:** Axios configured with interceptors for auth token injection and global error handling.
- **Server State Management:** `@tanstack/react-query` is utilized for caching, synchronizing, and updating server state efficiently without complex Redux boilerplate.
- **Form Handling:** `react-hook-form` used for performant, uncontrolled form validation.
- **Routing:** `react-router-dom` handles client-side routing.

## 3. Directory Structure (`src/`)

```
src/
├── api/          # Axios instance config, interceptors, and API wrappers
├── assets/       # Static assets (images, fonts, global CSS variables)
├── components/   # Reusable UI components
│   ├── charts/   # Recharts wrappers
│   ├── common/   # Generic buttons, modals, badges, loaders
│   ├── feedback/ # Toast notifications, alerts
│   ├── forms/    # Input fields, selects, date-pickers mapped to react-hook-form
│   ├── layout/   # Sidebar, Navbar, Page wrappers
│   └── tables/   # Data grid components, pagination
├── contexts/     # React Context providers (e.g., AuthContext, ThemeContext)
├── hooks/        # Custom React hooks (e.g., useAuth, useFetch)
├── layouts/      # High-level layout wrappers (e.g., DashboardLayout, AuthLayout)
├── pages/        # Route-level components mapping directly to application views
│   ├── Dashboard/
│   ├── Inventory/
│   ├── Login/
│   ├── Products/
│   ├── Profile/
│   ├── Reports/
│   ├── Settings/
│   ├── Users/
│   └── Work/
├── routes/       # Route definitions and Guard components (ProtectedRoutes)
├── services/     # Business logic helpers or API service abstractions
├── styles/       # Global CSS (e.g., index.css, App.css)
├── utils/        # Helper functions (date formatting, string manipulation)
├── App.jsx       # Root React component providing Contexts and Router
└── main.jsx      # Vite entry point, rendering React tree to the DOM
```

## 4. State Management Strategy
The application divides state into two categories:
1. **Server State:** Managed by `React Query`. Data fetched from the FastAPI backend is cached, automatically re-fetched when stale, and updated optimistically during mutations.
2. **Client State / Global UI State:** Managed by native React Context. Examples include the current authenticated user's session (`AuthContext`) and sidebar collapse state.
3. **Local State:** Managed by `useState` and `useReducer` inside individual components for ephemeral data (e.g., dropdown open/close).

## 5. Security Implementations (Frontend)
- **Route Guards:** Implementation of `ProtectedRoute` components that verify the presence and validity of the JWT token before rendering sensitive pages.
- **Role-Based Rendering:** UI elements (like "Edit" or "Delete" buttons) conditionally render based on the permissions array attached to the user's JWT payload or fetched profile.
- **Token Management:** JWT is stored securely (typically localStorage or sessionStorage) and attached to every outgoing request via Axios interceptors. Upon receiving a 401 Unauthorized, the interceptor automatically triggers a logout flow.

## 6. Styling Approach
- **TailwindCSS:** Almost all styling is handled via Tailwind utility classes directly in the `className` prop.
- **Component Extraction:** Repeated utility class combinations are either abstracted into React components (e.g., `<Button variant="primary">`) or customized in `index.css` via `@apply` directives for global elements.
