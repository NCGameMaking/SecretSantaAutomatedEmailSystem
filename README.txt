# The Automated Secret Santa Email System

A web application built using **Python (Flask)** and **HTML5/CSS3** that automated the process of organising a Secret Santa.

Users can set an event date, a budget and add participants by providing their name and email. The system then processes the algorithm to shuffle up the participants and launch private. holiday themed cards through email directly to each person's inbox without revealing pairing to anybody.

---

 ## Features:

 * Add or remove player rows dynamically on the frontend through JavaScript.
 * Raw date picking and numeric budget fields that allow data to be smoothly transferred to the backend.
 * A conditional loop that ensures no participant is ever assigned to themselves.
 * Implements environmental variable masking (`.env`) for private mail configurations.
 * A full-screen loading animation to show users that the script is loading/working in the backend even though the frontend is frozen
 * Sends styled holiday card layouts through a secure background SMTP connection to GMAILs servers.