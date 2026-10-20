# Publicação do Ateliê OS

Leia o [README](README.md) para instalação e configuração completa. Nunca envie `.env`, bancos locais, arquivos de clientes ou credenciais ao repositório.

## Render

1. Conecte o repositório ao Render e publique pelo `render.yaml`.
2. Defina `ADMIN_PASSWORD` antes da primeira criação de banco. Render gera `SECRET_KEY` pelo Blueprint; mantenha-a estável.
3. Configure `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET` como variáveis protegidas e cadastre no Google Cloud Console o callback HTTPS `/auth/google/callback` do domínio Render.
4. O Blueprint usa SQLite e disco persistente; mantenha backups externos. PostgreSQL gerenciado pode ser usado com `DATABASE_URL`. Anexos também precisam de volume persistente e privado.
5. Cadastre contas e perfis em **Usuários e acessos**. O login Google só aceita e-mails previamente cadastrados e verificados.

## Vercel

Use PostgreSQL gerenciado via `DATABASE_URL`. O filesystem da função é efêmero; configure armazenamento persistente para anexos. Siga as variáveis e o callback descritos no README e em `INSTRUCOES_VERCEL.md`.

Após a publicação, valide os principais fluxos em um ambiente de teste. Habilite HTTPS, backups e revise privacidade, retenção de arquivos e os modelos de documentos antes de operar com dados reais. O repositório sozinho não hospeda o backend Flask.
