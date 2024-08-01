
# SMTP Communication Report

## SMTP Communication Sequence:
- **Frame 60:** The server (smtp.gmail.com) sends a "220" response indicating that it is ready to start communication. The message contains the ESMTP (Extended Simple Mail Transfer Protocol) identifier and a unique session identifier.
- **Frame 62:** The client sends the "EHLO" command to introduce itself and request extended SMTP capabilities from the server.
- **Frame 74:** The server responds with a "250" message, listing its capabilities.
- **Frame 76:** The client sends mail.

## Key Information:

- **SMTP Protocol:** Used for sending emails.
- **EHLO Command:** Extended HELO, used to identify the sending server and request ESMTP capabilities.
- **STARTTLS Command:** Used to initiate a secure (encrypted) connection using TLS.
- **Response Codes:**
  - **220:** Server is ready.
  - **250:** Request command completed successfully.
  - **220 2.0.0:** Server is ready to start TLS.
