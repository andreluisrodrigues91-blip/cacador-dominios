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

    dominios_para_testar = [
        "solarvendas.com.br"
    ]

    for dominio in dominios_para_testar:
        prompt = f"Avalie o domínio '{dominio}' para revenda em 2 linhas. Diga se o potencial é Alto ou Baixo."
        
        try:
            # Usando o modelo padrão estável
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            resultado = response.text
            
            msg = f"🌐 Domínio: {dominio}\n\n📋 Análise:\n{resultado}"
            enviar_telegram(msg)
            
        except Exception as e:
            print(f"❌ Erro ao processar {dominio}: {e}")

if __name__ == "__main__":
    analisar_dominios()
