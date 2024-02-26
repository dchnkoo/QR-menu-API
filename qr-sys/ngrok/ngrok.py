from pyngrok import ngrok
from app.settings import origins
import os


env = os.environ

AUTH_TOKEN = env.get("NGROK_AUTHTOKEN", None)

if AUTH_TOKEN is not None:
    PORT = env.get("NGROK_PORT", "5173")
    HOST = env.get("NGROK_HOST", "127.0.0.1")

    ngrok.set_auth_token(AUTH_TOKEN)
    
    tunnel = ngrok.connect(f"{HOST}:{PORT}", "http")
    

    url = tunnel.public_url

    print(f"""\n\n\n\n\n
    ##          ##          ## ##       ## ## ##             ## ## ##        ##       ##
    ####        ##       ##       ##    ##      ##         ##        ##      ##     ##
    ##  ##      ##     ##          ##   ##       ##      ##            ##    ##   ##
    ##    ##    ##    ##                ##      ##      ##              ##   ## ## 
    ##      ##  ##    ##      ## ##     ## ## ##        ##              ##   ##   ##
    ##        ####    ##           ##   ## ##            ##            ##    ##     ##
    ##          ##     ##     ## ##     ##   ##            ##        ##      ##       ##
    ##          ##      ## ## ##        ##     ##            ## ## ##        ##         ##
          
    URL {url} -> http://{HOST}:{PORT}
    \n\n\n\n\n
    """)

    try:
        origins.remove("*")
    except:
        pass

    origins.append(url)
    
    while True:
        ...
    






