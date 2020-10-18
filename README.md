# Overview
This module allows users to automatically create their own personal voice channel upon joining a temporary channel titled `CLICK TO JOIN VC`

# Commands Usage
- `-setup` -> Automatically sets up the room creation module in the server
- `-lock` -> Locks the current voice channel to prevent users from joining
- `-unlock` -> Unlocks the current voice channel for users to join
- `-allow <user>` -> Grants access to specified user to join the voice channel after channel is locked
- `-deny <user>` -> Deny specified user from joining the public voice channel
- `-kick <user>` -> Kicks specified user out of the voice channel into an AFK channel titled `💤 AFK`
- `-claim` -> Claims the ownership of current voice channel after owner has left

# Notes
- All commands are usable only in a text channel titled `command-logs`
- Room creation module is only executable under the category titled `🎤 Custom Channels`
- Tweak and configure the category/channel name accordingly to your preference in the script by replacing CTRL+F and replace the default name stated above.
