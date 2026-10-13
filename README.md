# FF Ban Check - Free Fire Ban Checker API & Web Tool

A lightweight, fast, and modern web application + REST API to check Free Fire account ban status and duration by querying Garena's official Anti-Hack verification system.

Developed and maintained by **[Refat Rahman](https://refat.ovh)**.

---

## 🚀 Features

- **🌐 Interactive Web Interface**: Sleek, mobile-friendly gaming UI (`templates/index.html`) to check UIDs directly in your browser.
- **⚡ Direct Garena Anti-Hack Verification**: Real-time ban status and ban duration directly from Garena's official servers.
- **🔑 API Key Authentication**: Built-in simple token access management (`/check_key` and `/bancheck`).
- **🛡️ CORS Enabled**: Ready to be integrated into web and mobile applications.
- **☁️ Vercel Serverless Ready**: Includes `vercel.json` for one-click deployment.

---

## 🛠️ Installation & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/refatbd/ff-ban-check.git
cd ff-ban-check
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python app.py
```
Open your browser and navigate to: `http://127.0.0.1:5000`

---

## 📖 API Documentation

### 1. Web Page & API Information
- **Web UI:** `GET /` (Opens interactive web interface)
- **API Info:** `GET /api` or `GET /?format=json`
- **Response:**
```json
{
  "service": "Free Fire Ban Check API",
  "name": "FF Ban Check",
  "status": "online",
  "developer": {
    "name": "Refat Rahman",
    "website": "https://refat.ovh",
    "github": "https://github.com/refatbd",
    "facebook_id": "https://www.facebook.com/rjrefat/",
    "facebook_page": "https://www.facebook.com/fb.refat.ovh",
    "instagram": "https://www.instagram.com/refat_official",
    "telegram": "https://t.me/refatbd",
    "whatsapp": "+8801747032300"
  },
  "endpoints": {
    "/bancheck": "Check player ban status (requires key & uid)",
    "/check_key": "Verify API key",
    "/developer": "Developer profile and contact details"
  }
}
```

---

### 2. Verify API Key
- **Endpoint:** `GET /check_key?key=<YOUR_KEY>`
- **Example:** `http://127.0.0.1:5000/check_key?key=refatbd`
- **Response:**
```json
{
  "status": "valid",
  "key_status": "active",
  "developer": {
    "name": "Refat Rahman",
    "website": "https://refat.ovh",
    "github": "https://github.com/refatbd",
    "facebook_id": "https://www.facebook.com/rjrefat/",
    "facebook_page": "https://www.facebook.com/fb.refat.ovh",
    "instagram": "https://www.instagram.com/refat_official",
    "telegram": "https://t.me/refatbd",
    "whatsapp": "+8801747032300"
  }
}
```

---

### 3. Check Player Ban Status
- **Endpoint:** `GET /bancheck?key=<YOUR_KEY>&uid=<PLAYER_UID>`
- **Parameters:**
  - `key` *(required)*: Authorized API key (`refatbd` or `refat`)
  - `uid` *(required)*: Free Fire Player UID
- **Example:** `http://127.0.0.1:5000/bancheck?key=refatbd&uid=5384583894`
- **Response:**
```json
{
  "developer": "Refat Rahman",
  "github": "https://github.com/refatbd",
  "website": "https://refat.ovh",
  "uid": "5384583894",
  "is_banned": true,
  "status": "BANNED",
  "ban_period": 6
}
```

---

### 4. Developer Profile
- **Endpoint:** `GET /developer`

---

## 🌐 Deploy to Vercel

1. Push this repository to GitHub under `https://github.com/refatbd/ff-ban-check`.
2. Go to [Vercel](https://vercel.com/) and click **Add New Project**.
3. Select your repository and deploy. The included `vercel.json` will automatically configure the Python serverless runtime.

---

## 👨‍💻 Developer & Contact

| Platform | Link / Contact |
| :--- | :--- |
| **Name** | Refat Rahman |
| **Website** | [refat.ovh](https://refat.ovh) |
| **GitHub** | [@refatbd](https://github.com/refatbd) |
| **Facebook Profile** | [rjrefat](https://www.facebook.com/rjrefat/) |
| **Facebook Page** | [fb.refat.ovh](https://www.facebook.com/fb.refat.ovh) |
| **Instagram** | [@refat_official](https://www.instagram.com/refat_official) |
| **Telegram** | [@refatbd](https://t.me/refatbd) |
| **WhatsApp** | [+8801747032300](https://wa.me/8801747032300) |

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).