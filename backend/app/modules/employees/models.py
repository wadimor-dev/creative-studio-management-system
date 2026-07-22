"""EmployeeProfile is deprecated. Use sub-models from app.core.organization instead:

  - EmployeeContact    → contact info (phone, address)
  - EmployeeEducation  → education records
  - EmployeeBank       → bank/payroll info
  - EmployeeEmergencyContact → emergency contact
  - EmployeeDocument   → uploaded documents

These are defined in:
  app.core.organization.employee_contact.models.EmployeeContact
  app.core.organization.employee_education.models.EmployeeEducation
  app.core.organization.employee_bank.models.EmployeeBank
  app.core.organization.employee_emergency_contact.models.EmployeeEmergencyContact
  app.core.organization.employee_document.models.EmployeeDocument
"""
