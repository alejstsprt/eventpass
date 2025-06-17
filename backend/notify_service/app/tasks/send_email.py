from email.message import EmailMessage

import aiosmtplib

from backend.notify_service.config import config


async def send_email(to: str, title: str, text: str):
    message = EmailMessage()
    message["From"] = config.EMAIL
    message["To"] = to
    message["Subject"] = title
    message.add_alternative(
        f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f6f8; margin:0; padding:20px;">
            <table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px; margin:auto; background:#ffffff; border-radius:8px; box-shadow:0 0 10px rgba(0,0,0,0.1);">
            <tr>
                <td style="padding: 30px; text-align: center; background-color: #121212; border-bottom: 1px solid #eaeaea; border-radius: 8px 8px 0 0;">
                <h1 style="margin:0; font-weight:700; font-size: 32px; font-family: 'Arial Black', Arial, sans-serif;">
                    <span style="color: #03DAC6;">event</span><span style="color: #FFFFFF;">pass</span>
                </h1>
                </td>
            </tr>
            <tr>
                <td style="padding: 30px; color: #333333; font-size: 16px; line-height: 1.5;">
                {text}
                </td>
            </tr>
            <tr>
                <td style="padding: 20px; text-align: center; font-size: 12px; color: #999999; border-top: 1px solid #eaeaea; border-radius: 0 0 8px 8px;">
                © 2025 EventPass. Все права защищены.
                </td>
            </tr>
            </table>
        </body>
        </html>
        """,
        subtype="html",
    )

    await aiosmtplib.send(
        message,
        hostname="smtp.mail.ru",
        port=587,
        username=config.EMAIL,
        password=config.PASSWORD_KEY,
        start_tls=True,
    )
    print(f"[✔] Сообщение отправилось на почту {to}. Заголовок: {title}")
