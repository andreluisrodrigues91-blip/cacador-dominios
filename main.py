import os
import requests
import google.generativeai as genai

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def analisar_dominios():
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    dominios_para_testar = [
        "solarvendas.com.br",
        "advocaciabrasil24h.com.br",
        "clinicasorrirmais.com.br",
        "cursonoturno123.com.br"
    ]

    for dominio in dominios_para_testar:
        prompt = f"""
        Avalie o domínio '{dominio}' para revenda (Domain Flipping) no Brasil.
        Responda em formato curto e direto:
        1. Potencial Comercial (Baixo, Médio, Alto)
        2. Quem seriam os potenciais compradores locais ou empresas?
        3. Estimativa realista de valor de revenda (em R$).
        4. Há risco de violação de marca registrada?
        """
        
        try:
            response = model.generate_content(prompt)
            resultado = response.text
            
            if "Alto" in resultado or "Médio" in resultado:
                msg = f"🎯 *OPORTUNIDADE DE DOMÍNIO ENCONTRADA!*\n\n🌐 *Domínio:* `{dominio}`\n\n📋 *Análise da IA:*\n{resultado}\n\n💡 *Ação:* Custa ~R$ 40 no Registro.br para registrar."
                enviar_telegram(msg)
        except Exception as e:
            print(f"Erro ao processar {dominio}: {e}")

if __name__ == "__main__":
    analisar_dominios()
