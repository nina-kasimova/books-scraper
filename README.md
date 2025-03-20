# 📚 Books Scraper Frontend  

This is the **React/Next.js** frontend for the **Books Scraper** project, a web application that allows users to **build, manage, and populate book lists by scraping Goodreads**.  

## 🎯 Purpose  
The goal of this project is to showcase **full-stack development skills** by integrating **web scraping, a REST API, and an interactive UI**.  

### This project is useful for:  
- ✅ **Book lovers** who want to organize their reading lists  
- ✅ **Portfolio demonstration** of working with **FastAPI, Next.js, and external APIs**  
- ✅ **Learning project** for API interactions, data handling, and UI design  

---

## 🛠 Tech Stack  
- **Frontend:** Next.js (React), TypeScript, Tailwind CSS  
- **UI Components:** ShadCN UI, Material UI (MUI)  
- **Backend (separate repo):** Python, FastAPI, SQLAlchemy, PostgreSQL  
- **Data Handling:** Axios (API requests), Web Scraping (backend)  

---

## 🚀 Features  
- **📋 View Books Table:** Displays books in a sortable and searchable table  
- **🔗 Scrape Books:** Enter a Goodreads list URL and scrape books into your database  
- **📂 Manage Lists:** Create, view, and filter books by lists  
- **⚡ Fast & Responsive UI** using Tailwind and modern UI libraries  

---

## 🔗 Backend Integration  
This frontend interacts with a **FastAPI backend** to handle book data.  

### API Endpoints Used  
- `GET /books` → Fetch all books  
- `POST /scrape` → Scrape books from a Goodreads list  
- `GET /lists` → Fetch all book lists  
- `GET /get_book_byList?list_id={id}` → Fetch books from a specific list  

---

## 🖥 Setup & Installation  

### Prerequisites  
Ensure you have:  
- **Node.js 18+**  
- **npm** or **yarn**  

### Installation  
```sh
git clone https://github.com/yourusername/books-scraper.git  
cd books-scraper  
npm install  # or yarn install  
npm run dev
