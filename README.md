NaadanRoute: AI-Powered Kerala Travel Ecosystem

**NaadanRoute** is a sophisticated, full-stack travel platform designed to connect travelers ("Sancharis") with authentic Kerala travel experiences.
Moving beyond traditional CRUD applications, it features **Kera**, a RAG-powered GenAI concierge, a secure administrative dashboard, and a fully integrated financial pipeline.

## 🚀 Key Technical Highlights

* **GenAI Integration (Kera):** A personality-driven chatbot utilizing **Gemini 1.5 Flash** and **RAG (Retrieval-Augmented Generation)** to match user emotions and needs with real-time package data.
* **Role-Based Access Control (RBAC):** A custom-built admin suite ("Navigator") featuring granular permissions using Django decorators to separate Staff and Superuser capabilities.
* **Transaction Engineering:** Secure payment processing via **Razorpay API** with server-side integrity checks and automated invoice generation.
* **Data Intelligence:** Advanced filtering, aggregate sales analytics, and CSV data export functionality for business operations.

---

## 🛠️ The Tech Stack

| Layer | Technology |
| --- | --- |
| **Backend** | Django (Python) |
| **Frontend** | HTML5, CSS3, JavaScript (Django Template Engine) |
| **Artificial Intelligence** | Gemini 2.5 Flash API, RAG Architecture |
| **Database** | PostgreSQL / SQLite |
| **Payments** | Razorpay Integration |
| **Security** | RBAC, Custom Decorators, Session-based Memory |

---

## 📁 Project Structure Highlights

```text
├── NaadanRoute/      # Core project configuration & security settings
├── accounts/         # User Authentication & Profile Management
├── navigator/        # Administrative Dashboard & Logic
├── tours/            # Travel Package Engines
├── media/            # Dynamic user-uploaded travel assets
└── static/           # Global CSS, JS, and UI frameworks
```
🧠 Feature Deep-Dive

### 1. Kera: The RAG-Lite Chatbot

Unlike standard bots, Kera uses **Context Injection**.

* **Intent Detection:** Analyzes if a user is seeking adventure, relaxation, or culture.
* **Dynamic Context:** The backend fetches available packages from the SQL database and injects them into the LLM prompt.
* **Structured Output:** Uses regex and JSON parsing to extract a `suggested_package_id`, allowing the UI to highlight specific tours directly from the conversation.

### 2. The Navigator (Admin Dashboard)

A comprehensive suite for managing business operations:

* **Sales Analytics:** Real-time calculation of Monthly Active Users (MAU), total revenue, and order volume using Django `Sum` and `Count` aggregates.
* **Inventory Management:** Full CRUD for Categories, Sub-categories, Blogs, and Travel Packages with multi-media support.
* **Order Fulfillment:** Workflow management from "Ordered" to "Completed" with the ability to export audit-ready CSV reports.

### 3. Traveler Features

* **Culture Compass:** A specialized calendar tracking upcoming cultural events in Kerala.
* **Personalized Profile:** Dashboard for users to track previous orders, wishlists, and bucket lists.
* **Booking Engine:** Multi-step booking flow including headcount calculation, address management, and secure checkout.

---

## 🔒 Security Implementation

The project implements a strict security hierarchy in `urls.py`:

* **`staff_member_required`**: Grants read-access to dashboards and invoices for employees.
* **`superuser_only`**: Custom decorator restricting destructive actions (Delete/Edit) and financial settings to top-level admins only.

---

## 🏗️ Installation & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/NaadanRoute.git
cd NaadanRoute

```


2. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


3. **Environment Variables:**
Create a `.env` file and add your credentials:
```env
GEMINI_API_KEY=your_key_here
RAZORPAY_KEY_ID=your_id_here
RAZORPAY_KEY_SECRET=your_secret_here
SECRET_KEY=your_django_secret

```


4. **Run Migrations & Start:**
```bash
python manage.py migrate
python manage.py runserver

```



---

## 📈 Future Roadmap

* **Vector Database Migration:** Moving from SQL-context injection to **ChromaDB** or **Pinecone** for scaling to thousands of packages.
* **Asynchronous Tasks:** Integrating **Celery/Redis** for background payment captures and automated email invoices.
* **Interactive Maps:** Mapbox integration for visual itinerary tracking.
