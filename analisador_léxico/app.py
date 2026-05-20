import re
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Inicializa o FastAPI
app = FastAPI(title="Lexical Engine")

# Configura a pasta de templates (onde está o seu index.html)
templates = Jinja2Templates(directory="templates")

# Definindo a Gramática: Padrões Regex para os tokens
TOKEN_REGEX = [
    ('COMMENT', r'//.*|/\*[\s\S]*?\*/'),           
    ('WHITESPACE', r'\s+'),                        
    ('KEYWORD', r'\b(if|else|while|for|return|int|float|void|print)\b'), 
    ('NUMBER', r'\b\d+(\.\d+)?\b'),                
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'), 
    ('OPERATOR', r'[+\-*/=<>!&|]+'),               
    ('SYMBOL', r'[(){}\[\],;]'),                   
    ('MISMATCH', r'.'),                            
]

# --- A LÓGICA PERMANECE INTACTA ---
def analyze_code(code: str):
    tokens = []
    symbol_table = {}
    eliminated = []
    pos = 0
    line = 1

    while pos < len(code):
        match = None
        for token_type, regex in TOKEN_REGEX:
            pattern = re.compile(regex)
            match = pattern.match(code, pos)
            
            if match:
                value = match.group(0)
                if token_type == 'WHITESPACE':
                    line += value.count('\n')
                    eliminated.append({'type': 'Espaço/Quebra de Linha', 'value': repr(value)})
                elif token_type == 'COMMENT':
                    line += value.count('\n')
                    eliminated.append({'type': 'Comentário', 'value': value})
                elif token_type == 'MISMATCH':
                    tokens.append({'type': 'ERRO_LEXICO', 'value': value, 'line': line})
                else:
                    tokens.append({'type': token_type, 'value': value, 'line': line})
                    if token_type == 'IDENTIFIER':
                        if value not in symbol_table:
                            symbol_table[value] = {'type': 'Variável/Função', 'lines': [line]}
                        elif line not in symbol_table[value]['lines']:
                            symbol_table[value]['lines'].append(line)
                pos = match.end()
                break
                
        if not match:
            pos += 1

    return tokens, symbol_table, eliminated


# --- AQUI COMEÇAM AS MUDANÇAS DO FASTAPI ---

# 1. Pydantic Model: Define exatamente o que o backend espera receber
class CodeRequest(BaseModel):
    code: str

# 2. Rota GET para renderizar a interface
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Nas versões mais recentes do FastAPI/Starlette, o 'request' precisa ser nomeado assim:
    return templates.TemplateResponse(request=request, name="index.html")
    
# 3. Rota POST para a análise léxica
@app.post("/analyze")
async def analyze(data: CodeRequest):
    # O FastAPI já valida automaticamente se 'data.code' existe e é uma string!
    tokens, symbol_table, eliminated = analyze_code(data.code)

    return {
        'tokens': tokens,
        'symbol_table': [{'name': k, 'details': v} for k, v in symbol_table.items()],
        'eliminated': eliminated
    }