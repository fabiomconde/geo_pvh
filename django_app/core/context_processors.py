import os

def ngrok_url(request):
    """
    Injeta a URL pública do ngrok, se existir, 
    no contexto de todas as páginas Django.
    """
    return {
        'ngrok_public_url': os.environ.get('NGROK_PUBLIC_URL', '')
    }
