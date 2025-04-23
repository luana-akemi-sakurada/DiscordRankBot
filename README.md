# DiscordRankBot

A Discord bot for tracking player points, creating leaderboards, and enabling point transactions between users.

## Features

- **Point Management**: Add, remove, or set points for users (admin only)
- **Leaderboard System**: View a complete ranking of all players
- **Point Gifting**: Allow users to give points to each other
- **Individual Point Checking**: Users can check their own or others' point totals
- **Persistent Storage**: Points are saved between bot restarts

## Commands

| Command | Description | Example | Permission |
|---------|-------------|---------|------------|
| `!addpoints` | Add points to a user | `!addpoints @User 50` | Admin only |
| `!removepoints` | Remove points from a user | `!removepoints @User 10` | Admin only |
| `!setpoints` | Set a user's points to a specific value | `!setpoints @User 100` | Admin only |
| `!give` | Give some of your points to another user | `!give @User 25` | Anyone |
| `!points` | Check your points or someone else's | `!points` or `!points @User` | Anyone |
| `!leaderboard` or `!lb` | Show the complete server leaderboard | `!leaderboard` | Anyone |
| `!resetleaderboard` | Reset the entire leaderboard (requires confirmation) | `!resetleaderboard` | Admin only |

## Setup Instructions

1. **Install Python** (version 3.8 or newer)
2. **Install dependencies**:
   ```
   pip install discord.py
   ```
3. **Create a Discord bot**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application and add a bot
   - Enable the "Message Content Intent" and "Server Members Intent"
   - Copy your bot token

4. **Configure the bot**:
   - Replace `YOUR_TOKEN_HERE` in `ranking_bot.py` with your actual bot token
   
5. **Invite the bot to your server**:
   - Generate an invite URL in the OAuth2 section of the Developer Portal
   - Select the "bot" scope and appropriate permissions

6. **Run the bot**:
   ```
   python ranking_bot.py
   ```

## Data Storage

The bot stores all ranking data in a file called `leaderboard.json`. This file is automatically created when the bot first runs and is updated whenever points change.

## Requirements

- Python 3.8 or newer
- discord.py library
- A Discord server with appropriate permissions
