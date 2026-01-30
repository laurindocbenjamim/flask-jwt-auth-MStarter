# flask-jwt-auth-MStarter

This is a starter page with JWT authentication modules.

# API Documentation

This document provides a detailed overview of the available endpoints in the Flask JWT Auth application.

## Authentication API
**Base URL:** `/api/v1/auth`

### 1. Login
- **Endpoint:** `/login`
- **Method:** `POST`
- **Description:** Authenticate a user and return an access token (and set cookies).
- **Request Body:**
  ```json
  {
    "username": "user@example.com",
    "password": "yourpassword"
  }
  ```
- **Response (Success - 200):**
  ```json
  {
    "status_code": 200,
    "message": "User logged successfull!",
    "username": "user@example.com",
    "registered_as": "normal"
  }
  ```
  *Note: Sets `access_token_cookie`.*

### 2. Logout (Token Revocation)
- **Endpoint:** `/logout`
- **Method:** `GET`, `DELETE`
- **Description:** Revokes the current access token by adding it to the blocklist.
- **Headers:** `Authorization: Bearer <access_token>`
- **Response (Success - 200):**
  ```json
  {
    "msg": "Access token successfully revoked",
    "logout": "Your session has been terminated!",
    "block_list": { ... }
  }
  ```

### 3. Test Create User
- **Endpoint:** `/test-create`
- **Method:** `GET`
- **Description:** Creates a test admin user (hardcoded in code).
- **Response:** JSON with creation status.

---

## User API
**Base URL:** `/api/v1/user`

### 1. Register User
- **Endpoint:** `/dao`
- **Method:** `POST`
- **Description:** Register a new user.
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "username": "myuser",
    "password": "mypassword",
    "firstname": "John",
    "lastname": "Doe",
    "phone": "+123456789",
    "country": "Portugal",
    "address": "123 Street",
    "postal_code": "1234"
  }
  ```
- **Response (Success - 200):**
  ```json
  {
    "status_code": 200,
    "message": "User has been created successfull"
  }
  ```

### 2. Get User
- **Endpoint:** `/dao/<int:user_id>`
- **Method:** `GET`
- **Description:** Retrieve user details.
- **Response:**
  ```json
  {
    "status_code": 200,
    "user": { ... }
  }
  ```

### 3. Update User
- **Endpoint:** `/dao/<int:user_id>`
- **Method:** `PUT`
- **Description:** Update user details.
- **Headers:** `Authorization: Bearer <access_token>`
- **Request Body:** (Partial fields allowed)
  ```json
  {
    "name": "New Name",
    "username": "newuser",
    "email": "new@example.com",
    "phone": "999999999",
    "country": "Spain"
  }
  ```
- **Response:**
  ```json
  {
    "status_code": 200,
    "message": "User updated successfully",
    "user": { ... }
  }
  ```

### 4. Delete User
- **Endpoint:** `/dao/<int:user_id>`
- **Method:** `DELETE`
- **Description:** Delete a user.
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
  ```json
  {
    "status_code": 200,
    "message": "User deleted successfully"
  }
  ```

### 5. Email Confirmation
- **Endpoint:** `/dao/<token>`
- **Method:** `PATCH`
- **Description:** Confirm user email using a token from the link.
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
  ```json
  {
    "status_code": 200,
    "message": "Email confirmed"
  }
  ```

### 6. Get Users by Type
- **Endpoint:** `/get-users/<string:usertype>`
- **Method:** `GET`
- **Description:** Get all users of a specific type (except 'admin').
- **Response:**
  ```json
  {
    "success": true,
    "data": [ ... ]
  }
  ```

### 7. User Management (Admin)
- **Endpoint:** `/manager`
- **Method:** `GET`
- **Description:** Get all users (Admin only).
- **Headers:** `Authorization: Bearer <access_token>` (Admin privileges required)
- **Response:**
  ```json
  {
    "status_code": 200,
    "users": [ ... ]
  }
  ```
- **Other Methods on `/manager` or `/manager/<id>`:** `PUT`, `DELETE`, `PATCH` (Currently return placeholder strings "updated", "deleted", "confirmed").

---

## Google Auth (`Auth2`)
**Base URL:** `/api/v1/auth2`

### 1. Index
- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Renders index page with login status.

### 2. Login Page Info
- **Endpoint:** `/login`
- **Method:** `GET`
- **Description:** Returns Google Client ID.

### 3. Google Sign-In
- **Endpoint:** `/google/signin`
- **Method:** `POST`
- **Description:** Verifies Google ID token.
- **Request Body (Form Data):** `id_token=<token>`
- **Response:**
  ```json
  {
    "success": true,
    "redirect": "/"
  }
  ```

### 4. Logout
- **Endpoint:** `/logout`
- **Method:** `GET`
- **Description:** Clears session and redirects to index.

---

## Admin API
**Base URL:** `/api/v1/admin`

### 1. User Data
- **Endpoint:** `/user`
- **Method:** `GET`
- **Description:** Returns currently logged-in user data and administration flags.
- **Headers:** `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "status_code": 200,
    "message": "Welcome to protected route!",
    "is_administrator": true,
    "full_name": "...",
    ...
  }
  ```

### 2. Admin User Info
- **Endpoint:** `/adm_user`
- **Method:** `GET`
- **Description:** Returns simple admin check info (Admin only).
- **Headers:** `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "status_code": 200,
    "message": "Welcome to the Admin route!"
  }
  ```

### 3. Manage Users
- **Endpoint:** `/manage-user`
- **Method:** `GET`, `PUT`, `DELETE`, `PATCH`
- **Description:** Admin endpoints for user management (list, update, delete).
- **Headers:** `Authorization: Bearer <token>`

---

## Email Services API
**Base URL:** `/api/v1/email`

### 1. Send Confirm Email (SendGrid)
- **Endpoint:** `/send-confirm`
- **Method:** `POST` (Implied from Resource)
- **Description:** Sends a confirmation email using SendGrid.

### 2. Send Confirm Email to New User
- **Endpoint:** `/send-confirm-to-new-user`
- **Method:** `POST` (Implied from Resource)
- **Description:** Sends a confirmation email to a newly registered user.

### 3. Send Email (SendGrid)
- **Endpoint:** `/send`
- **Method:** `POST` (Implied from Resource)
- **Description:** Generic email sending endpoint via SendGrid.

### 4. Confirm Email (Link Target)
- **Endpoint:** `/confirm_email`
- **Method:** `GET`
- **Description:** Endpoint that users hit when clicking the confirmation link.
- **Query Params:** `token=<jwt_token>`
- **Response:** Renders `success_email_confirm.html` with success or error message.

---

## Author Profile API
**Base URL:** `/profile`

### 1. Projects
- **Endpoint:** `/laurindo-c-benjamim/projects`
- **Method:** `GET`
- **Description:** Renders the author's projects page (`projects.html`).

### 2. Experiences
- **Endpoint:** `/laurindo-c-benjamim/experiences`
- **Method:** `GET`
- **Description:** Renders the author's experiences page (`experiences.html`).

### 3. About
- **Endpoint:** `/laurindo-c-benjamim`
- **Method:** `GET` (via URL Rule)
- **Description:** Renders the author's about page (`about.html`).

---

## General / Root Routes

### 1. Home
- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Renders the landing page.

### 2. Login (No Cookies)
- **Endpoint:** `/login_without_cookies`
- **Method:** `POST`
- **Request Body:** `{"username": "...", "password": "..."}`
- **Response:** Returns `access_token` in JSON body.

### 3. Login (With Cookies)
- **Endpoint:** `/login-w-cookies`
- **Method:** `POST`
- **Request Body:** `{"username": "...", "password": "..."}`
- **Response:** Sets `access_token_cookie`.

### 4. Logout (With Cookies)
- **Endpoint:** `/logout_with_cookies`
- **Method:** `POST`
- **Description:** Unsets JWT cookies.

### 5. Logout (Revoke Token)
- **Endpoint:** `/logout-with-revoking-token`
- **Method:** `POST`
- **Headers:** `Authorization: Bearer <token>`
- **Description:** Revokes the current token.

### 6. Protected Route
- **Endpoint:** `/protected`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <token>`
- **Response:** Returns user claims and info.

### 7. Test Token
- **Endpoint:** `/test-token`
- **Method:** `POST`
- **Request Body:** `{"token": "..."}`
- **Description:** Decodes and verifies a JWT token.

### 8. Generate Secret Key
- **Endpoint:** `/secret-key/gen`
- **Method:** `GET`
- **Description:** Generates a random secret key.

### 9. Test Email
- **Endpoint:** `/test_send_email`
- **Method:** `GET`
- **Description:** Sends a test email.

### 10. Debug Config
- **Endpoint:** `/debug-config/<dev>`
- **Method:** `GET`
- **Description:** Returns config variables if `dev` matches config.

---

## Troubleshooting

### Common Errors

#### 1. 404 Not Found: Favicon (`/favicon.ico`)
**Error Log:**
```
INFO - 192.168.1.209 - - [29/Jan/2026 13:19:21] "GET /favicon.ico HTTP/1.1" 404 -
werkzeug.exceptions.NotFound: 404 Not Found: The requested URL was not found on the server.
```

**Cause:**
Browsers automatically request `favicon.ico` to display the site icon. If Flask is not configured to serve this file from the root, it returns a 404 error.

**Solution:**
Add a specific route to serve the favicon from your static assets directory.

```python
from flask import send_from_directory
import os

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'assets', 'img', 'favicon'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
```
*Ensure the file exists at the specified path (`src/static/assets/img/favicon/favicon.ico`).*

#### 2. Docker Error: Address Already in Use
**Error Log:**
```
Error response from daemon: driver failed programming external connectivity on endpoint ...
failed to bind host port for 0.0.0.0:5432:172.22.0.2:5432/tcp: address already in use
```

**Cause:**
Port 5432 on your host machine is already being used (likely by a local PostgreSQL installation), preventing Docker from binding the container's port to it.

**Solution:**
Modify `docker-compose.yml` to map the container's port 5432 to a different host port (e.g., 5433).

```yaml
services:
  db:
    ports:
      - "5433:5432"  # Change host port to 5433
```
*Then rebuild:* `docker-compose up --build`

#### 3. Flask-Limiter Warning: In-memory Storage
**Warning Log:**
```
UserWarning: Using the in-memory storage for tracking rate limits as no storage was explicitly specified.
```

**Cause:**
`Flask-Limiter` requires a storage backend (like Redis or Memcached). If none is configured, it falls back to in-memory storage, which resets when the application restarts.

**Solution:**
Explicitly configure the storage URI in `src/config.py` (e.g., to `memory://` to suppress the warning if in-memory is intended, or a valid Redis URL).

```python
# In src/config.py
RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')
```

#### 4. SQLAlchemy Error: Missing Database URI
**Error Log:**
```
Error: Either 'SQLALCHEMY_DATABASE_URI' or 'SQLALCHEMY_BINDS' must be set.
```

**Cause:**
The `SQLALCHEMY_DATABASE_URI` configuration variable is evaluating to `None` or an empty string, likely because the `DATABASE_URL` environment variable is present but empty, or the default fallback wasn't triggering correctly.

**Solution:**
Ensure `SQLALCHEMY_DATABASE_URI` has a valid fallback value in `src/config.py`.

```python
# In src/config.py
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or 'sqlite:///development.db'
```
This ensures that if `DATABASE_URL` is empty, the default SQLite database is used.
