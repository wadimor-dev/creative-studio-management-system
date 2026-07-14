# Test Cases (WA-08)

## 1. Authentication & Users
| ID | Scenario | Expected Result | Status |
|---|---|---|---|
| AUTH-01 | Login valid credentials | Token returned | PASSED |
| AUTH-02 | Login invalid credentials | 401 Unauthorized | PASSED |
| AUTH-03 | Expired token | 401 Expired | PASSED |
| USER-01 | Create user valid | 201 Created | PASSED |
| USER-02 | Create user existing username | 400 Bad Request | PASSED |

## 2. Inventory & Stock
| ID | Scenario | Expected Result | Status |
|---|---|---|---|
| INV-01 | Add new Item | Item created, stock 0 | PASSED |
| INV-02 | Add stock | Stock increased | PASSED |
| INV-03 | Transfer stock | Stock correctly moved | PASSED |

## 3. Work Activity (Core Flow)
| ID | Scenario | Expected Result | Status |
|---|---|---|---|
| WA-01 | Create Activity | Status READY | PASSED |
| WA-02 | Start without BEFORE photo | ERROR (Validation) | PASSED |
| WA-03 | Start with BEFORE photo | Status WORKING | PASSED |
| WA-04 | Upload PROGRESS | Photo saved | PASSED |
| WA-05 | Finish without AFTER photo | ERROR (Validation) | PASSED |
| WA-06 | Finish with AFTER photo | Status COMPLETED | PASSED |
| WA-07 | Create Activity while another is WORKING | ERROR (Validation) | PASSED |

## 4. Asset Integration (Borrow/Return)
| ID | Scenario | Expected Result | Status |
|---|---|---|---|
| ASSET-01 | Borrow valid stock | Stock reduced, asset logged | PASSED |
| ASSET-02 | Borrow exceeding stock | ERROR (Validation) | PASSED |
| ASSET-03 | Auto return on Finish | Stock restored | PASSED |

## 5. Analytics & Export
| ID | Scenario | Expected Result | Status |
|---|---|---|---|
| RPT-01 | Fetch reports Daily | 200 OK | PASSED |
| RPT-02 | Export PDF as Employee | 403 Forbidden | PASSED |
| RPT-03 | Export Excel as Admin | File downloaded, log created | PASSED |

