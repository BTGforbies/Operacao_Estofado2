# Publicação do Ateliê OS

Leia o [README](README.md) para instalação e configuração completa. Nunca envie `.env`, bancos locais, arquivos de clientes ou credenciais ao repositório.

## PythonAnywhere gratuito (Flask com SQLite)

1. Crie uma conta gratuita Beginner e adicione uma web app por **Manual configuration**, usando Python 3.11 ou superior.
2. No Bash Console, clone a branch publicada e instale as dependências em um ambiente virtual:

   ```bash
   git clone -b codex/google-auth-security https://github.com/BTGforbies/Operacao_Estofado2.git ~/estofado
   cd ~/estofado
   mkvirtualenv estofado --python=python3.13
   pip install -r requirements.txt
   ```

3. No arquivo WSGI da web app, adicione o caminho do projeto ao `sys.path`, configure `SECRET_KEY`, `ADMIN_PASSWORD`, `APP_ENV=production`, `HTTPS=1`, `APP_DB` e `UPLOAD_DIR`, e importe `app` como `application`. Mantenha banco e uploads em uma pasta privada da conta fora do checkout Git. Chame `init_db()` após configurar as variáveis na primeira inicialização.
4. Configure `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET` no arquivo WSGI (fora do repositório) e adicione ao Google Cloud Console o callback `https://SEU_USUARIO.pythonanywhere.com/auth/google/callback`. O login local funciona sem essas credenciais.
5. Cadastre usuários e perfis em **Usuários e acessos**. O login Google aceita somente e-mails previamente cadastrados e verificados.

A conta gratuita oferece 512 MiB de disco e uma web app com um worker. O site gratuito expira após um mês e precisa ser renovado manualmente. O acesso de saída à internet é limitado a uma lista de domínios; GitHub, Google e Google APIs constam na lista atual, mas teste o fluxo OAuth após a publicação. Consulte as limitações atuais antes de usar o sistema.

## Render gratuito (demonstração)

1. Conecte o repositório ao Render e publique pelo `render.yaml`, selecionando a branch `codex/google-auth-security`.
2. Defina `ADMIN_PASSWORD` antes da primeira criação do banco. O Blueprint gera `SECRET_KEY`; mantenha-a estável.
3. O plano gratuito usa filesystem efêmero e suspende o serviço após inatividade. O SQLite e os anexos locais podem ser apagados quando o serviço dormir, reiniciar ou receber novo deploy. Use apenas para demonstração com dados descartáveis.
4. O login local fica disponível. Para login Google, configure `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET` como variáveis protegidas e cadastre no Google Cloud Console o callback HTTPS `/auth/google/callback` do domínio Render.

Para operar com dados que precisam persistir, use um serviço com armazenamento persistente e configure PostgreSQL via `DATABASE_URL` e armazenamento persistente para anexos. Isso pode exigir um plano pago.

## Vercel

Use PostgreSQL gerenciado via `DATABASE_URL`. O filesystem da função é efêmero; configure armazenamento persistente para anexos. Siga as variáveis e o callback descritos no README e em `INSTRUCOES_VERCEL.md`.

Após a publicação, valide os principais fluxos em um ambiente de teste. Habilite HTTPS, backups e revise privacidade, retenção de arquivos e os modelos de documentos antes de operar com dados reais. O repositório sozinho não hospeda o backend Flask.
