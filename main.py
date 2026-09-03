import os
import requests
import google.generativeai as genai

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    # Removido o parse_mode Markdown para evitar erros de formatação
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}
    
    resposta = requests.post(url, json=payload)
    dados = resposta.json()
    
    if not dados.get("ok"):
        print(f"❌ ERRO DO TELEGRAM: {dados}")
    else:
        print("✅ Mensagem enviada com sucesso para o Telegram!")

def analisar_dominios():
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    dominios_para_testar = [
        "solarvendas.com.br",
        "advocaciabrasil24h.com.br"
    ]

    for dominio in dominios_para_testar:
        prompt = f"Avalie o domínio '{dominio}' para revenda em 3 linhas."
        
        try:
            response = model.generate_content(prompt)
            resultado = response.text
            
            # Envia TODAS as análises sem filtro para testar a conexão
            msg = f"🌐 Domínio: {dominio}\n\n📋 Análise:\n{resultado}"
            enviar_telegram(msg)
            
        except Exception as e:
            print(f"❌ Erro ao processar Gemini: {e}")

if __name__ == "__main__":
    analisar_dominios()
