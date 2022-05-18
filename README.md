# Basic Discord Bot With Cogs
### Features
- Basic Moderation
- can ban, kick or mute (vis-versa)
- Uses embeds for asthetics
- makes a DB for every guild it interacts with collections corresponding to bans, kicks and mutes.
    ```python
    #ex with muting a user makes a tree like <guild> -> usersMuted -> <user>:
    {"_id": int(member.id), "author": str(ctx.author), "usermuted": str(member.name+"#"+member.discriminator), "reason": reason, "time": time, "date": datetime.datetime.utcnow()}
    ```
### Installation

```bash
pip install -r requirements.txt
```

### Getting Started
*This bot uses MongoDB for storage* - [MongoDB](https://www.mongodb.com/)
- Add your own DB to your local env variables
- Tutorial on how to create a Db with mongo Atlas: [here](https://www.mongodb.com/docs/atlas/getting-started/)

**Tips:**
- make a env file with your local DB
- Anything that involves the DB should have DB_ as var name 
    ```env
    #ex of env file
    DB_URL=<URL>
    DB_DB=<DB_NAME>
    #ect...
    ```
- If you want to use a local DB, you can use the `local` DB_URL