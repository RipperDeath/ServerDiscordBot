# Basic Discord Bot With Cogs

*This bot uses MongoDB for storage* - [MongoDB](https://www.mongodb.com/)
- Add your own DB to your local env variables
- Tutorial on how to create a Db with mongo Atlas: [here](https://www.mongodb.com/docs/atlas/getting-started/)

## Installation

```bash
pip install -r requirements.txt
```

# Getting Started

*tips:*
- make a env file with your local DB
- Anything that involves the DB should have DB_ as var name 
```env
DB_URL=<URL>
DB_DB=<DB_NAME>
ext...
```
- If you want to use a local DB, you can use the `local` DB_URL