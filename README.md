# CRM de Secretaria Escolar

Sistema inicial para gestão de secretaria escolar com:

- Login com níveis de acesso (`admin`, `secretaria`, `professor`);
- Importação de alunos a partir de planilha Excel;
- Listagem de alunos;
- Geração de documentos escolares (Declaração e Ficha SOME).

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Acesse `http://localhost:5000`.

### Usuário padrão

- **E-mail:** `admin@escola.local`
- **Senha:** `admin123`

## Formato da planilha

A planilha deve conter as colunas:

- `matricula`
- `nome`
- `turma`
- `data_nascimento` (opcional)
- `responsavel` (opcional)

## Próximos passos sugeridos

- Cadastro de funcionários e perfis de acesso por permissões granulares;
- Geração de documentos em PDF com assinatura digital;
- Histórico escolar e diário de classe;
- Auditoria de ações por usuário.
