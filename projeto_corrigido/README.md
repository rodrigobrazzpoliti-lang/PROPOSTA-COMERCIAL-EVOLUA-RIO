# Projeto Evolua Rio - Versão Corrigida para Vercel

## Estrutura do Projeto

```
projeto_corrigido/
├── api/
│   ├── index.py          # Arquivo principal da API
│   ├── models/           # Modelos do banco de dados
│   ├── routes/           # Rotas da API
│   └── database/         # Arquivos do banco
├── static/               # Build do frontend React
├── requirements.txt      # Dependências Python
├── vercel.json          # Configuração da Vercel
└── .vercelignore        # Arquivos a ignorar no deploy
```

## Como Fazer o Deploy

1. **Preparar o Frontend:**
   - Faça o build do projeto React
   - Copie os arquivos de `dist/` para `static/`

2. **Fazer Upload:**
   - Faça upload desta pasta corrigida para seu repositório
   - Ou use a CLI da Vercel: `vercel --prod`

3. **Configurar Variáveis de Ambiente (se necessário):**
   - No painel da Vercel, adicione as variáveis necessárias

## Principais Correções Aplicadas

1. ✅ Estrutura de pastas compatível com Vercel
2. ✅ Arquivo `api/index.py` como ponto de entrada
3. ✅ Configuração correta do `vercel.json`
4. ✅ Imports ajustados para funcionar na Vercel
5. ✅ Tratamento de erros para imports
6. ✅ Rota de health check para testes

## Testando Localmente

```bash
cd projeto_corrigido
pip install -r requirements.txt
python api/index.py
```

A API estará disponível em `http://localhost:5000`

## Rotas Disponíveis

- `GET /api/health` - Verificação de saúde da API
- `GET /api/users` - Listar usuários
- `POST /api/users` - Criar usuário
- `POST /api/proposal/generate` - Gerar proposta
- `GET /proposta/<id>` - Visualizar proposta

## Observações

- O banco SQLite será criado automaticamente
- Para produção, considere usar PostgreSQL
- Certifique-se de que o build do React esteja na pasta `static/`

