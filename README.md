# MollyTech Inventory Analytics

A web-based inventory analytics management system developed for a small buy-and-sell business to manage inventory, sales, revenue, and profit through a centralized system.

The system provides a centralized platform for recording inventory, managing sales, tracking product status, and analyzing business performance through automated calculations and analytics.

## Features

### Inventory Management

- Add and edit products
- Product search
- Inventory filtering
- Available and sold status tracking
- Product archiving
- Inventory value calculation
- Expected profit calculation

### Sales Management

- Record product sales
- Automatic profit calculation
- Automatic revenue calculation
- Inventory status updates
- Sales history
- Daily and monthly sales tracking
- Total profit tracking
- Top-performing product and brand tracking

### Analytics

- Total products
- Available stock
- Completed sales
- Revenue analytics
- Profit analytics
- Sales performance graphs
- Product performance
- Brand performance
- Business summaries

### Authentication

- Administrator authentication
- Password hashing
- Password recovery
- Email-based password reset

## Technology Stack

- Python
- Flask
- HTML5
- CSS3
- JavaScript
- PostgreSQL
- psycopg2-binary
- Jinja2

## Database

The application uses **PostgreSQL** as its relational database.

The database stores inventory records, sales information, user accounts, authentication data, and business analytics used by the application.

## Requirements

- Windows
- Python 3.12+
- PostgreSQL
- Git
- Web Browser

## Running the Project

1. Clone the repository.
2. Install the required Python dependencies.
3. Configure the PostgreSQL database.
4. Configure the application's environment variables.
5. Start the Flask application.

```bash
python app.py
```

> The project is currently configured for a local development environment and may require additional configuration depending on the user's machine.

## Project Structure

```text
MollyTech Inventory Analytics Management System/
│
├── cli/
│   ├── db.py
│   ├── inventory.py
│   ├── main.py
│   ├── reports.py
│   ├── sales.py
│   └── __init__.py
│
├── static/
│   ├── css/
│   ├── images/
│   └── js/
│
├── templates/
├── app.py
├── hash_password.py
├── .env.example
├── .gitignore
└── README.md
```

## Project Status

**Functional Portfolio Project**

The system is currently functional and has been tested locally.

The current version is intended for personal business management and portfolio demonstration. Additional security testing, deployment testing, scalability improvements, and mobile testing would be required before production use.

Future improvements include expanded analytics, notifications, improved authentication and security, API integration, public deployment, and potential customer-facing ordering functionality.

## Developer Role

**Full Stack Developer**

Responsible for:

- System design
- Frontend development
- Backend development
- Python and Flask development
- PostgreSQL database integration
- Authentication
- Business analytics
- Inventory and sales functionality
- System integration
- Functional testing

## Author

**Ralph Michael M. Molina**

GitHub: [Mollytovvv](https://github.com/Mollytovvv)
