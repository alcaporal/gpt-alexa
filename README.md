# GPT Alexa v0.1
Versão base da skill Alexa para acionar o chatGPT. Estamos usando o modelo gpt-4o, mas outros estão disponíveis mantendo a mesma estrutura via openai >=1.0.0

## !IMPORTANTE!
A chave api está hardcode, recomendado utilizar como variável de ambiente no painel da AWS Lambda.

Nessa versão toda vez que a função generate_gpt_response for chamada, a conversa começará com o prompt_instructions como mensagem de sistema, ou seja, um “briefing” para o agente (que escolherá um nome) se comportar do jeitinho que você quer.

Além disso, a função está atualizando esse messages com os novos turnos (user e assistant), o que mantém o contexto da conversa localmente, desde que a Lambda não seja encerrada entre interações.

Se a Lambda "esfriar" (timeout ou nova instância), você perde o histórico da conversa. 
O modelo do OpenAI tem um limite de contexto. Como estamos guardando todas as interações em messages, isso pode estourar se a conversa se estender.

Essa skill é básica como exemplo, podendo ser implementado outros recursos como integrações de outros sistemas, funcionalidades e armazenamento para manter o histórico entre sessões.
