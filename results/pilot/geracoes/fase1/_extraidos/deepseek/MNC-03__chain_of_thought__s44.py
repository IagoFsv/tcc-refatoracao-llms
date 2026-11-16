def _create_completion(text):
    return openai.Completion.create(
        model="text-davinci-002",
        prompt=text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

def _extract_choices(completion):
    return completion["choices"]

def _extract_text_from_choice(choice):
    return choice["text"].strip("  \n")

def summarize(text):
    """Summarize a text string and return a summary of the text"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = _create_completion(text)
    choices = _extract_choices(completion)
    text = _extract_text_from_choice(choices[0])
    return text

def executar(texto, escolhas):
    """Resume texto; devolve o resumo e os pedidos feitos. Ponto de entrada publico desta unidade."""
    Completion.pedidos = []
    Completion.escolhas = list(escolhas)
    resumo = summarize(texto)
    return resumo, Completion.pedidos
