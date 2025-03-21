# discord-reel-poster
Takes IG Reel links from chat and posts the mp4 video file to chat.

## Configuration

Only the `DISCORD_BOT_TOKEN` environment variable needs to be configured with the Discord bot token. See Discord documentation for this.

## Logging

```log
[2025-03-21 04:22:26] [WARNING ] discord.client: PyNaCl is not installed, voice will NOT be supported
[2025-03-21 04:22:26] [INFO    ] discord.client: logging in using static token
[2025-03-21 04:22:27] [INFO    ] discord.gateway: Shard ID None has connected to Gateway (Session ID: SESSION_ID).
[2025-03-21 04:22:29] [INFO    ] discord: Logged in as Reel Poster - BOT_ID
[2025-03-21 04:22:37] [INFO    ] discord: Post submitted for USER(USER_ID) in #DM(DM_ID): https://www.instagram.com/reel/aAbBcCdDeE/
```
