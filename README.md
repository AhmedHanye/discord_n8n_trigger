# Discord N8N Trigger
![alt text](images/project.png)

# Guide
This guide will help you set up and use this simple Discord n8n message trigger.
- [N8N Setup](#n8n-setup)
- [Discord Bot Setup](#discord-bot-setup)
- [Workflow Setup](#workflow-setup)
- [Deploy the Trigger](#deploy-the-trigger)
- [Contributing](#contributing)

## N8N Setup

1. [Set Up a VPS](https://youtu.be/F-9KWQByeU0?si=idrEg3JvuCxr23Pd)
2. [Install n8n on your VPS](https://docs.n8n.io/getting-started/installation/)
3. [Video guide](https://youtu.be/ONgECvZNI3o?si=n_-jegtGBtzs9BZB)
4. [Use template](https://n8n.io/workflows/3456-automated-discord-chatbot-for-chat-interaction-in-channel-using-gemini-20-flash/)

## Discord Bot Setup

1. Create a new application in the [Discord Developer Portal](https://discord.com/developers/applications).
2. Add a bot to your application and copy the bot token.
3. Invite the bot to your server with the appropriate permissions.

## Workflow Setup

1. Create a new workflow in n8n.
2. Configure the webhook node to receive messages from Discord Trigger.
    - Set the HTTP Method to POST.
    - Set credentials for the webhook
3. Configure the rest of the workflow as needed.

## Deploy the Trigger

1. Create a `.env` file in the root of your project and add the following environment variables:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   N8N_WEBHOOK_URL=your_n8n_webhook_url
   N8N_BASIC_AUTH_USER=your_n8n_username
   N8N_BASIC_AUTH_PASSWORD=your_n8n_password
   ```
2. Build and run the Docker container using Docker Compose:
   ```bash
   docker-compose up -d
   ```
3. Verify that the bot is running and connected to your Discord server.
4. Test the trigger by sending a message in the Discord channel where the bot is present.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes you'd like to make.
