import os
import requests
from google import genai

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}
    
    resposta = requests.post(url, json=payload)
    dados = resposta.json()
    
    if not dados.get("ok"):
        print(f"❌ ERRO DO TELEGRAM: {dados}")
    else:
        print("✅ Mensagem enviada com sucesso para o Telegram!")

def analisar_dominios():
    client = genai.Client(api_key=GEMINI_API_KEY)

    dominios_para_testar = [
        "solarvendas.com.br",
        "advocaciabrasil24h.com.br",
        "clinicasorrirmais.com.br"
    ]

    for dominio in dominios_para_testar:
        prompt = f"""
        Avalie o domínio '{dominio}' para revenda em 3 linhas.
        Responda se o Potencial é Alto, Médio ou Baixo e uma sugestão rápida de venda.
        """
        
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            resultado = response.text
            
            msg = f"🌐 Domínio: {dominio}\n\n📋 Análise da IA:\n{resultado}"
            enviar_telegram(msg)
            
        except Exception as e:
            print(f"❌ Erro ao processar {dominio}: {e}")

if __name__ == "__main__":
    analisar_dominios()
