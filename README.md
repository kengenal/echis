# Echis - discord bot
Discord bot written in python using discordpy lib

## features
* play music
* send meme from reddit
* bad words filter
* register user
* login to web app
* share your playlist, if you add to your playlsit bot automatically send to discord server 

## How to run
###you need create channels 
* admin
* meme
* music
* start
* share
* login - only for web application

### Next you need set your bot token in system environment variable

```bash
export TOKEN="your token"
```

## Additional environment variables
```bash
export PREFIX="prefix"
export BOT_NAME="your bot name"
```

## Share module environment variables
```bash
export TOKEN_SECRET="your secret to generate token"
export TOKEN_ALGORITHM="set jwt algorithm"
export EXP="token lifetime"
export WEB="host for web app"
```

## Web app
```bash
export PREFIX="prefix"
export BOT_NAME="your bot name"
```



* command to run bot

```bash
python main.py
```

## License
[GNU GPLv3](https://github.com/kengenal/echis/blob/master/LICENSE)
