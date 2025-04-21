import logging
import ask_sdk_core.utils as ask_utils
from openai import OpenAI
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

# Configuração OpenAI
client = OpenAI(api_key="Insira sua chave da API Open AI aqui")
model_configurado = "gpt-4o"
max_tokens_configurado = 1000
temperature_configurado = 0.85

# Configuração agente 
seu_nome = "Insira seu nome ou como gostaria de ser chamado aqui"
agent_nome = "Insira o nome de seu agente aqui"
prompt_instructions = """Você é um assistente pessoal com o objetivo ajudá-lo em diversos aspectos da vida, assumindo papel de especialista em temas relacionados as suas perguntas considerando além do tema, o tipo ou formato de conteúdo solicitado, o objetivo explicito e buscando responder de forma clara, concisa e usando uma linguagem simples em Português do Brasil. 
Procure incorporar um estilo humano, com contrações, expressões idiomáticas, frases de transição, interjeições, modificadores e coloquialismos, ao mesmo tempo em que usa dispositivos literários como simbolismos, ironia, prenúncio, metáfora, personificação, hipérbole, aliteração, imagens, onomatopéias, e símile sem mencioná-los diretamente. 
Você pode sugerir informações complementares além do que foi solicitado quando achar que pode ser extremamente relevante para ele considerando sua personalidade, contexto de vida entre outras características que serão descritas a seguir:
Características físicas: 
Características psicológicas: 
Características de relacionamento: 
Características de hobbies: 
Características ideológicas: 
Características profissionais: 
"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

messages = [{"role": "system", "content": prompt_instructions}]

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = f"Oi {seu_nome}, aqui é {agent_nome}. O que deseja?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class GptQueryIntentHandler(AbstractRequestHandler):
    """Handler for Gpt Query Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GptQueryIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        query = handler_input.request_envelope.request.intent.slots["query"].value
        response = generate_gpt_response(query)

        return (
                handler_input.response_builder
                    .speak(response)
                    .ask("Alguma outra pergunta?")
                    .response
            )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors."""
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Desculpe, não consegui obter uma resposta para esta pergunta. Tente perguntar de outra forma."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Até mais. Se cuida!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
    
def generate_gpt_response(query):
    try:
        messages.append({"role": "user", "content": query})
        response = client.chat.completions.create(
            model=model_configurado,
            messages=messages,
            max_tokens=max_tokens_configurado,
            temperature=temperature_configurado
        )
        reply = response.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GptQueryIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
