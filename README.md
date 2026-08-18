# MollyTech Service Desk


- Administrator dashboard
- User management
- Technician management
- Ticket monitoring
- System activity monitoring
- Administrative settings


## Technology Stack


### Frontend


- React
- Vite
- JavaScript
- HTML5
- CSS3
- Framer Motion
- Recharts


### Backend


- Node.js
- Express.js
- Socket.IO
- JWT
- bcrypt


### Database


- MongoDB
- Mongoose


### Development Tools


- Git
- GitHub
- Visual Studio Code


## System Architecture


The application follows a full-stack client-server architecture.


The React frontend communicates with the Node.js and Express backend through REST APIs, while Socket.IO provides real-time communication for messaging, notifications, and live system updates.


MongoDB is used as the primary database for storing users, tickets, conversations, messages, notifications, and related system data.


## Database


The application uses **MongoDB** as its primary database.


The database stores:


- User accounts
- Roles and permissions
- Support tickets
- Ticket assignments
- Conversations
- Messages
- Notifications
- System-related records


## Project Structure


```text
MollyTech Service Desk System/
│
├── backend/
│   ├── src/
│   │   ├── controllers/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── routes/
│   │   └── ...
│   │
│   ├── uploads/
│   ├── server.js
│   └── package.json
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── ...
│   │
│   ├── public/
│   └── package.json
│
├── .gitignore
├── README.md
└── ...
Project Status

Functional Full-Stack Portfolio Project

The system is currently functional and has been tested during development.

The project is primarily intended for portfolio demonstration and software engineering practice.

Additional security testing, production deployment hardening, scalability testing, monitoring, and infrastructure configuration would be required before production use.

Developer Role

Full Stack Developer

Responsible for:

System architecture
Frontend development
Backend development
REST API development
MongoDB database integration
Authentication and authorization
Role-based access control
Real-time communication
Ticket management workflows
Messaging system
Notification system
System integration
Debugging
Functional testing
Author

Ralph Michael M. Molina

GitHub: Mollytovvv
