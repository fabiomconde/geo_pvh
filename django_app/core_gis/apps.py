from django.apps import AppConfig
import sys
import os

class CoreGisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_gis'
    verbose_name = 'Observatório de Conflitos Socioambientais e Direitos Humanos - Porto Velho'
    verbose_name_plural = 'Observatórios de Conflitos Socioambientais e Direitos Humanos - Porto Velho'

    def ready(self):
        # Evita abrir múltiplos ngrok tunnels em reloads (ex: worker thread do gunicorn ou dev server)
        # O ngrok deve iniciar apenas no processo principal de roteamento runserver do Django (evita sys.argv migrations etc)
        if os.environ.get('RUN_MAIN') == 'true' and 'runserver' in sys.argv:
            try:
                from pyngrok import ngrok, conf

                # Start ngrok tunnel on port 8000 with auth
                ngrok.set_auth_token("6o1VwvnAHhM4dD2LNW6xU_4TTCH95bMqXBy3QY6SnSq")
                options = {"auth": "plataforma:pvh2026!", "bind_tls": True}
                
                active_tunnels = ngrok.get_tunnels()
                if active_tunnels:
                    public_url = active_tunnels[0].public_url
                    print(f"==================================================")
                    print(f"⚡ NGROK TUNNEL ALREADY ACTIVE: {public_url}")
                    print(f"==================================================")
                else:
                    # Desconecta túneis anteriores pra evitar limite de conta grátis
                    ngrok.kill()
                    
                    # Inicia túnel na porta configurada, default 8000
                    port = sys.argv[sys.argv.index('runserver') + 1] if len(sys.argv) > sys.argv.index('runserver') + 1 else "8000"
                    if port.startswith('0.0.0.0:'):
                        port = port.split(':')[1]

                    public_url = ngrok.connect(port, **options).public_url
                    print(f"==================================================")
                    print(f"🚀 NGROK TUNNEL INITIALIZED: {public_url}")
                    print(f"🔒 Credentials -> User: plataforma / Pass: pvh2026!")
                    print(f"==================================================")
                
                # Injeta a variável env pro Django considerar durante o requests a APIs internas via URL absoluta, se houver
                os.environ["NGROK_PUBLIC_URL"] = public_url

            except Exception as e:
                print(f"⚠️ Failed to initialize ngrok tunnel: {e}")
