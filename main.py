import os
import requests
from google import genai

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def enviar_telegram(mensagem):
    chat_id_limpo = str(TELEGRAM_CHAT_ID).strip()
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN.strip()}/sendMessage"
    payload = {"chat_id": chat_id_limpo, "text": mensagem, "parse_mode": "Markdown"}
    
    resposta = requests.post(url, json=payload)
    dados = resposta.json()
    
    if not dados.get("ok"):
        print(f"❌ ERRO DO TELEGRAM: {dados}")
    else:
        print("✅ Mensagem enviada com sucesso para o Telegram!")

def analisar_dominios():
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Lista de alvos para varredura diária de alta conversão
    dominios_para_testar = [
        "solarvendas.com.br",
        "advocaciabrasil24h.com.br",
        "clinicasorrirmais.com.br"
    ]

    for dominio in dominios_para_testar:
        prompt = f"""
        Aja como um vendedor de elite especialista em Domain Flipping agressivo no Brasil.
        Avalie o domínio '{dominio}' e crie um dossiê comercial para fechar a venda rapidamente com um empresário do setor.
        Responda obrigatoriamente estruturado em:
        1. Potencial Comercial (Baixo, Médio ou Alto).
        2. Perfil do Comprador Ideal (quem precisa disso hoje).
        3. Script de Abordagem Comercial Ultra-Agressivo: um texto pronto para o usuário copiar e enviar via WhatsApp/E-mail ao empresário, usando forte escassez (prazo de 48h), proteção de marca e alerta de prejuízo por roubo de tráfego de concorrentes.
        """
        
        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
            )
            resultado = response.text
            
            msg = f"🎯 *ALVO DE DOMÍNIO DETECTADO*\n\n🌐 *Domínio:* `{dominio}`\n\n{resultado}"
            enviar_telegram(msg)
            
        except Exception as e:
            print(f"❌ Erro ao processar {dominio}: {e}")

if __name__ == "__main__":
    analisar_dominios()
