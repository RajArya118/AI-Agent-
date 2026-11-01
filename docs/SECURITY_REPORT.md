# BuildPilot AI — Security & Threat Modeling Report (Phase 7)

**Date:** 2026-11-01  
**Project:** BuildPilot AI  
**Author:** Security Engineering Specialist  

---

## 1. Security Posture Summary

| Security Domain | Control Implemented | Status |
|---|---|---|
| **API Key Protection** | Zero client-side leakage; keys strictly held in server `.env` | **PASSED** |
| **Path Traversal Protection** | Canonical resolve boundaries in `WorkspaceManager.validate_safe_path` | **PASSED** |
| **Math Code Injection Prevention** | AST parser whitelisting, strict rejection of `eval()` | **PASSED** |
| **Consequential Action Gating** | User confirmation dialog required before destructive mutations | **PASSED** |
| **File Upload Hardening** | 10MB file limit, extension whitelist (`.pdf`, `.txt`, `.md`, `.csv`) | **PASSED** |
| **Input Validation** | Pydantic v2 data models enforcing strict types | **PASSED** |
| **CORS Configuration** | Restricted domain list with credentials support | **PASSED** |
| **Container Isolation** | Non-root, isolated Docker container execution | **PASSED** |

---

## 2. Threat Modeling & Defense Verification

### 2.1 Path Traversal Attack Defense
- **Threat:** An attacker crafts a URL such as `/api/projects/{id}/files/../../../../windows/system32/cmd.exe` or `../../etc/shadow` to read arbitrary host files.
- **Defense Implementation:** `WorkspaceManager.validate_safe_path` computes the canonical absolute path of the sandbox base directory and the target file using Python's `Path.resolve()`. If `str(target).startswith(str(base))` evaluates to `False`, execution immediately halts with:
  ```python
  raise ValueError(f"Security Alert: Path traversal attempt blocked: '{relative_path}'")
  ```
- **Verification:** Tested with both POSIX `../../etc/passwd` and Windows `..\..\windows\system32\calc.exe`. Both were blocked with 100% reliability.

### 2.2 AST-Based Safe Calculator Evaluation
- **Threat:** Remote Code Execution (RCE) via `eval("os.system('rm -rf /')")` or `__import__('subprocess')`.
- **Defense Implementation:** The calculator parses arithmetic into an Abstract Syntax Tree (`ast.parse`) and permits ONLY whitelisted math operators (`+`, `-`, `*`, `/`, `^`, `%`) and standard functions (`sqrt`, `sin`, `cos`, `tan`, `log`, `factorial`). Any node of type `Import`, `Call` (unwhitelisted), or `Attribute` is immediately rejected with a syntax error.
- **Verification:** Verified by unit tests.

### 2.3 Consequential Actions Security Gate
- **Threat:** An autonomous agent unintentionally wiping database records or deleting projects without human oversight.
- **Defense Implementation:** Destructive actions trigger `request_consequential_action`, which creates a `PendingAction` in the database and returns `status: "requires_confirmation"`. The assistant stops turn processing until the user explicitly clicks "Approve & Execute" or "Reject" in the frontend modal.

### 2.4 File Upload & Denial of Service (DoS) Controls
- **Chunked Stream Size Limit:** Stream uploads verify cumulative byte size in 64 KB chunks. If the stream exceeds `MAX_UPLOAD_SIZE_MB` (10MB), the temporary buffer is deleted and an HTTP 413 Payload Too Large error is raised immediately, preventing memory exhaustion.
- **Extension Whitelist:** Files without valid `.pdf`, `.txt`, `.md`, or `.csv` extensions are rejected prior to processing.
