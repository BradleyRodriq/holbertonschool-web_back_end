# Cookies and Local Storage

---

## Table of Contents

- [Creating Cookies with JavaScript](#creating-cookies-with-javascript)
- [Setting Specific Cookie Attributes](#setting-specific-cookie-attributes)
- [Reading Cookies with JavaScript](#reading-cookies-with-javascript)
- [Using js-cookie for Easy Cookie Manipulation](#using-js-cookie-for-easy-cookie-manipulation)
- [Browser Web Storage](#browser-web-storage)
- [Differences Between Local Storage and Session Storage](#differences-between-local-storage-and-session-storage)

---

## Creating Cookies with JavaScript

To create a cookie in JavaScript, use the `document.cookie` property. Cookies are stored as a string in the format `key=value`. 

### Example:

```javascript
document.cookie = "username=Bradley";
```

This creates a simple cookie named `username` with a value of `Bradley`.

---

## Setting Specific Cookie Attributes

When creating cookies, you can set additional attributes such as expiration date, path, domain, and security options.

### Example:

```javascript
document.cookie = "username=Bradley; expires=Fri, 31 Dec 2024 12:00:00 UTC; path=/";
```

### Common Cookie Attributes:
- **expires**: Sets the expiration date for the cookie.
- **path**: Restricts the cookie to a specific path on the site.
- **domain**: Specifies the domain for which the cookie is valid.
- **secure**: Ensures that the cookie is only sent over HTTPS.
- **SameSite**: Controls whether the cookie is sent with cross-origin requests (can be set to `Strict`, `Lax`, or `None`).

### Example with `SameSite` and `secure`:

```javascript
document.cookie = "username=Bradley; expires=Fri, 31 Dec 2024 12:00:00 UTC; path=/; SameSite=Lax; secure";
```

---

## Reading Cookies with JavaScript

To read cookies, access the `document.cookie` string, which contains all cookies for the current domain. You can parse the string to retrieve the desired cookie.

### Example:

```javascript
function getCookie(name) {
    let cookieArr = document.cookie.split("; ");
    for (let cookie of cookieArr) {
        let cookiePair = cookie.split("=");
        if (cookiePair[0] === name) {
            return cookiePair[1];
        }
    }
    return null;
}

let username = getCookie("username");
console.log(username); // Outputs: Bradley
```

---

## Using js-cookie for Easy Cookie Manipulation

The `js-cookie` library simplifies cookie manipulation. It allows you to create, read, and delete cookies without manually handling cookie strings.

### Installing js-cookie:

You can install it via npm:

```bash
npm install js-cookie
```

Or use a CDN in your HTML file:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-cookie/3.0.1/js.cookie.min.js"></script>
```

### Example: Creating a Cookie

```javascript
Cookies.set('username', 'Bradley', { expires: 7, path: '/' });
```

This sets a cookie that expires in 7 days.

### Example: Reading a Cookie

```javascript
let username = Cookies.get('username');
console.log(username); // Outputs: Bradley
```

### Example: Deleting a Cookie

```javascript
Cookies.remove('username');
```

---

## Browser Web Storage

The Web Storage API provides a way to store key-value pairs in the browser. There are two types of storage:

- **Local Storage**: Data is persisted across browser sessions.
- **Session Storage**: Data is cleared when the page session ends (i.e., when the tab is closed).

---

### Differences Between Local Storage and Session Storage

| Feature                | Local Storage                            | Session Storage                       |
|------------------------|------------------------------------------|---------------------------------------|
| **Persistence**         | Data persists even after the browser is closed. | Data is cleared when the tab is closed. |
| **Scope**               | Shared across all tabs from the same origin. | Available only to the current tab.    |
| **Capacity**            | Up to 5-10 MB, depending on the browser.  | Up to 5 MB, depending on the browser. |
| **Use Case**            | Store user preferences, tokens, etc. that need to persist between sessions. | Store temporary data for the duration of the session. |

---

### Example: Using Local Storage

#### Setting an Item:

```javascript
localStorage.setItem('username', 'Bradley');
```

#### Getting an Item:

```javascript
let username = localStorage.getItem('username');
console.log(username); // Outputs: Bradley
```

#### Removing an Item:

```javascript
localStorage.removeItem('username');
```

### Example: Using Session Storage

#### Setting an Item:

```javascript
sessionStorage.setItem('sessionId', '12345');
```

#### Getting an Item:

```javascript
let sessionId = sessionStorage.getItem('sessionId');
console.log(sessionId); // Outputs: 12345
```

#### Removing an Item:

```javascript
sessionStorage.removeItem('sessionId');
```

---

## Conclusion

Cookies and Web Storage are essential tools for managing user data in the browser. While cookies are useful for storing small amounts of data and are automatically sent with HTTP requests, web storage offers a more efficient and flexible way to store larger amounts of data locally on the user's device without affecting network traffic. The `js-cookie` library simplifies cookie manipulation, making it easier to set, read, and delete cookies.
