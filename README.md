Attempting to perform the InitializeDefaultDrives operation on the 'FileSystem' provider failed.
# Ateliê OS

Sistema de gestão para estofarias em Flask. Inclui clientes, catálogo, orçamentos, serviços, visitas, despesas, PDFs, anexos privados e auditoria, com isolamento por empresa e perfis `admin`, `owner` e `staff`.

## Instalação local

Requer Python 3.11+. Crie um ambiente virtual, instale as dependências e configure variáveis de ambiente antes de iniciar:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:SECRET_KEY = (& python -c "import secrets; print(secrets.token_urlsafe(48))")
$env:ADMIN_PASSWORD = "uma-senha-inicial-forte"
python app.py
```

Abra `http://127.0.0.1:5000`. O banco SQLite `estofados.db` e o diretório `uploads/` são criados na primeira inicialização. Defina `ADMIN_PASSWORD` antes do primeiro uso em uma base vazia. Não há senha inicial padrão. Guarde a chave `SECRET_KEY` e não a altere entre reinícios, pois ela assina os cookies de sessão.

## Login com Google

1. No Google Cloud Console, crie um projeto, configure a tela de consentimento OAuth e crie uma credencial **OAuth client ID** do tipo **Web application**.
2. Adicione `http://127.0.0.1:5000/auth/google/callback` como URI de redirecionamento autorizado para desenvolvimento. Em produção, use `https://SEU_DOMINIO/auth/google/callback`.
3. Configure `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET` no ambiente do servidor. O botão Google só aparece quando os dois estiverem definidos.
4. Um administrador deve provisionar cada e-mail em **Usuários e acessos**, escolher Google e definir empresa e perfil. A primeira autenticação vincula o identificador Google verificado ao usuário ativo. Contas não cadastradas, desativadas ou com e-mail não verificado não entram.

A integração usa OpenID Connect com os metadados oficiais do Google (`accounts.google.com`) e os escopos `openid email profile`. O estado OAuth é validado pela biblioteca Authlib. Não é necessário expor um endpoint de token nem armazenar token Google na sessão da aplicação.

## Banco de dados e dados

SQLite é adequado para desenvolvimento em uma única instância. Em produção, configure `DATABASE_URL` para PostgreSQL gerenciado, com TLS e backups. O código migra de forma aditiva as colunas de identidade Google na tabela existente `users`; não recria nem apaga os dados. Faça backup antes de atualizar. Dados SQLite existentes não migram automaticamente para PostgreSQL: exporte/migre a base antes de trocar `DATABASE_URL`.

Arquivos enviados ficam em `UPLOAD_DIR` e precisam de armazenamento persistente e privado. Em hospedagem com disco efêmero, configure um volume persistente; esta versão não integra storage de objetos. Os uploads são entregues autenticados, com nome aleatório e limite de 8 MiB.

## Configuração de produção

- Configure `SECRET_KEY` (mínimo 32 caracteres imprevisíveis), `ADMIN_PASSWORD` (somente para a criação inicial), `DATABASE_URL`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `APP_ENV=production`, `UPLOAD_DIR` persistente e HTTPS.
- Cadastre no Google o callback HTTPS exato usado pelo domínio público.
- Execute com um servidor WSGI, por exemplo `gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 wsgi:app`.
- Use um PostgreSQL e volume de arquivos com backups e controle de acesso apropriados. Não comite `.env`, banco, uploads ou segredos.

Configure os valores como variáveis protegidas no provedor. `.env.example` contém somente nomes e valores vazios. Nunca coloque credenciais reais em arquivos versionados.

## Controle de acesso e sessões

- Só usuários previamente provisionados podem entrar por senha ou Google; a autenticação Google exige e-mail verificado.
- Usuários `owner` e `staff` ficam vinculados a uma empresa; as consultas e operações verificam propriedade no servidor. `staff` não acessa financeiro, configurações ou auditoria.
- A conta `admin` administra as duas empresas e gerencia usuários.
- Os formulários POST usam token CSRF. Logout é POST e limpa a sessão. Cookies são `HttpOnly`, `SameSite=Lax` e `Secure` em produção; sessões duram até 12 horas. O status e o papel do usuário são relidos no banco a cada requisição, permitindo revogação de acesso.
- Ative HTTPS em produção. A aplicação define cabeçalhos de segurança e HSTS em modo de produção.

## Verificação

Após instalar as dependências, rode `python -m unittest discover -s tests` para os testes automatizados. O teste de integração OAuth contra o Google exige credenciais e uma URI de callback autorizada. Faça ainda um smoke test após configurar hospedagem, banco, HTTPS e credenciais OAuth.

## Limitações conhecidas

O login local não oferece redefinição de senha ou MFA. O sistema não possui rate limiting nem integração com storage de objetos. Reveja a política de retenção/privacidade e os modelos de documentos antes de usar dados pessoais reais.

