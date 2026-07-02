import resend

from app.core.config import settings

resend.api_key = settings.RESEND_APY_KEY


def email_verify(email_destino: str, lead_name: str, token: str):
    params = {
        "from": "Velas Magia <onboarding@resend.dev>",
        "to": [email_destino],
        "subject": "🕯️ Activa tu cupón de bienvenida",
        "html": f"""
            <h1>¡Hola! {lead_name}</h1>
            <p>Para recibir tu cupón del 10%, por favor confirma que este es tu correo:</p>
            <a href="http://localhost:8000/api/v1/email_verify/verify?token={token}" 
               style="background: #000; color: #fff; padding: 10px 20px;">
               Confirmar y Ver Cupón
            </a>
        """,
    }
    resend.Emails.send(params)
