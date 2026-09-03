import os
import requests
from google import genai

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def enviar_telegram(mensagem):
    # Garante que o chat_id seja limpo de espaços em branco
    chat_id_limpo = str(TELEGRAM_CHAT_ID).strip()
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN.strip()}/sendMessage"
    payload = {"chat_id": chat_id_limpo, "text": mensagem}
    
    resposta = requests.post(url, json=payload)
    dados = resposta.json()
    
    if not dados.get("ok"):
        print(f"❌ ERRO DO TELEGRAM: {dados}")
    else:
        print("✅ Mensagem enviada com sucesso para o Telegram!")

def analisar_dominios():
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Lista expansível de alvos para a sua máquina de vendas
    dominios_para_testar = [
        "solarvendas.com.br",
        "advocaciabrasil24h.com.br",
        "clinicasorrirmais.com.br"
    ]

    for dominio in dominios_para_testar:
        prompt = f"""
        Aja como um vendedor de elite especialista em Domain Flipping no Brasil. 
        Avalie o domínio '{dominio}' e forneça de forma direta:
        1. Potencial Comercial (Alto ou Baixo).
        2. Perfil do comprador ideal.
        3. Script de abordagem comercial agressivo com escassez de 48h para o empresário via WhatsApp.
        """
        
        try:
            # Usando o modelo estável validado
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
            )
            resultado = response.text
            
            msg = f"🎯 ALVO DETECTADO: {dominio}\n\n{resultado}"
            enviar_telegram(msg)
            
        except Exception as e:
            print(f"❌ Erro ao processar {dominio}: {e}")

if __name__ == "__main__":
    analisar_dominios()
