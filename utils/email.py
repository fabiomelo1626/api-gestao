import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.tokenSettings import settings
from email.mime.image import MIMEImage
import os

def enviar_email_com_link_reset(destinatario: str, link_reset: str, username: str):
    remetente = settings.EMAIL_USER
    senha = settings.EMAIL_PASSWORD

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🔐 Redefinição de senha"
    msg["From"] = remetente
    msg["To"] = destinatario

    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: auto; border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; background-color: #f9f9f9;">
                <h2 style="color: #1e88e5;">🔐 Redefinição de Senha</h2>
                <p>Olá <strong>{username}</strong>,</p>
                <p>Recebemos uma solicitação para redefinir a senha da sua conta no sistema de saúde pública da <strong>Marka Sistemas</strong>.</p>
                <p style="text-align: center; margin: 30px 0;">
                    <a href="{link_reset}" style="background-color: #1e88e5; color: white; padding: 12px 20px; border-radius: 6px; text-decoration: none; font-weight: bold;">
                        🔁 Redefinir Senha
                    </a>
                </p>
                <p>Se você não solicitou essa alteração, pode ignorar este e-mail com segurança. Sua senha permanecerá a mesma.</p>
                <br>
                <p>📩 Em caso de dúvidas, entre em contato com nossa equipe de suporte.</p>
                <p>Obrigado,<br><strong>Equipe Marka Sistema</strong></p>
            </div>
        </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())
    except Exception as e:
        raise Exception(f"Erro ao enviar e-mail: {str(e)}")

def enviar_email_boas_vindas(destinatario: str, senha: str, username: str, link: str):
    remetente = settings.EMAIL_USER
    senha_email = settings.EMAIL_PASSWORD

    msg = MIMEMultipart("related")
    msg["Subject"] = "🔑 DEV - SYSTEM - Primeiro acesso ao sistema para Gestão."
    msg["From"] = remetente
    msg["To"] = destinatario

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <!-- Card do email -->
        <div style="max-width: 600px; margin: auto; background-color: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.05); overflow: hidden;">

          <!-- Imagem ocupando 100% da largura do card -->
          <div style="width: 100%;">
            <img src="cid:sistema_saude" alt="Marka Sistemas" style="width: 100%; height: auto; display: block;">
          </div>

          <!-- Conteúdo do card -->
          <div style="padding: 30px;">
            <h2 style="color: #2c3e50;">🎉 Bem-vindo, usuário {username}!</h2>
            <p style="font-size: 16px; color: #333;">
              Sua conta foi criada com sucesso e você já pode acessar o sistema de <strong>saúde pública</strong> da <strong style="color: #2980b9;">Marka Sistemas</strong>.
            </p>
            <p style="font-size: 16px; color: #333;">Abaixo estão seus dados de acesso ao sistema:</p>

            <div style="max-width: 400px; margin: 40px auto; padding: 20px; background-color: #f0f4f8; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); color: #333;">
              <div style="margin-bottom: 15px; font-weight: bold; font-size: 15px; color: #1e3a8a;">🔑 Seus dados de acesso:</div>
              <div style="padding: 12px; background-color: #ffffff; border-radius: 8px; border: 1px solid #d0d7de;">
                <p style="margin: 8px 0; font-size: 14px;"><strong>👤 Usuário:</strong> {username}</p>
                <p style="margin: 8px 0; font-size: 14px;"><strong>🔐 Senha temporária:</strong> 
                  <span style="display: inline-block; background-color: #e2e8f0; padding: 6px 12px; border-radius: 6px; font-weight: bold; font-family: monospace;">{senha}</span>
                </p>
              </div>
            </div>

            <div style="text-align: center; margin: 30px 0;">
              <a href="https://181.224.24.33:3000/login" style="background-color: #2980b9; color: #fff; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-size: 16px; font-weight: bold;">
                ➡️ Acessar o Sistema
              </a>
            </div>

            <p style="font-size: 15px; color: #555;">
              <strong style="color: #F22424;">Atenção:</strong> no primeiro acesso, será necessário alterar sua senha temporária por uma nova senha de sua escolha.
            </p>

            <p style="font-size: 14px; color: #777; margin-top: 40px;">
              Se você não reconhece esse cadastro ou recebeu este e-mail por engano, apenas ignore esta mensagem.
            </p>

            <hr style="margin-top: 30px; border: none; border-top: 1px solid #ddd;" />
            <p style="font-size: 12px; color: #999; text-align: center;">
              Este é um e-mail automático. Por favor, não responda.
            </p>
          </div>
        </div>
      </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    # Adicionando a imagem embutida
    caminho_imagem = os.path.join("img", "gestao.png")
    with open(caminho_imagem, "rb") as f:
        img = MIMEImage(f.read())
        img.add_header("Content-ID", "<sistema_saude>")
        img.add_header("Content-Disposition", "inline")  # Inline evita anexos
        msg.attach(img)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remetente, senha_email)
            server.sendmail(remetente, destinatario, msg.as_string())
    except Exception as e:
        raise Exception(f"Erro ao enviar e-mail: {str(e)}")
