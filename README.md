# GH-900 Study

Site em Python (Flask) para estudar para o exame **GH-900 — GitHub Foundations**.

- **Tópicos**: resumos dos 7 domínios com links para a documentação oficial.
- **Cartões**: flashcards de termos e conceitos (marque como dominado).
- **Questões**: treino por tópico, em modo *Prática* (feedback imediato) ou *Simulado* (correção no final), incluindo questões de múltipla seleção e "refazer meus erros".
- O progresso é salvo apenas no `localStorage` do navegador.

> Conteúdo autoral e não oficial. Não contém questões reais do exame. Valide as habilidades avaliadas no
> [guia oficial](https://learn.microsoft.com/credentials/certifications/resources/study-guides/gh-900).

## Executar

```powershell
cd app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Acesse <http://127.0.0.1:5000>.

## Testes

```powershell
python -m unittest discover -s tests -v
```

## Estrutura

```
app.py              rotas e API (/api/questoes, /api/corrigir, /api/cartoes)
content/topics.py   resumos por domínio
content/questions.py banco de questões (adicione tuplas em _RAW)
content/flashcards.py cartões
templates/, static/ interface
tests/              testes de conteúdo e rotas
```

Para adicionar uma questão, inclua uma tupla `(tópico, enunciado, opções, [índices corretos], explicação)` em
`content/questions.py`; os testes validam a consistência.
