# Publicação do Ateliê OS

Leia o [README](README.md) para instalação e configuração completa. Nunca envie `.env`, bancos locais, arquivos de clientes ou credenciais ao repositório.

## Render gratuito (demonstração)

1. Conecte o repositório ao Render e publique pelo `render.yaml`, selecionando a branch `codex/google-auth-security`.
2. Defina `ADMIN_PASSWORD` antes da primeira criação do banco. O Blueprint gera `SECRET_KEY`; mantenha-a estável.
3. O plano gratuito usa filesystem efêmero e suspende o serviço após inatividade. O SQLite e os anexos locais podem ser apagados quando o serviço dormir, reiniciar ou receber novo deploy. Use apenas para demonstração com dados descartáveis.
4. O login local fica disponível. Para login Google, configure `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET` como variáveis protegidas e cadastre no Google Cloud Console o callback HTTPS `/auth/google/callback` do domínio Render.
5. Cadastre contas e perfis em **Usuários e acessos**. O login Google só aceita e-mails previamente cadastrados e verificados.

Para operar com dados que precisam persistir, use um serviço com armazenamento persistente e configure PostgreSQL via `DATABASE_URL` e armazenamento de arquivos persistente para anexos. Isso pode exigir um plano pago. Não use o plano gratuito acima para dados reais importantes.

## Vercel

Use PostgreSQL gerenciado via `DATABASE_URL`. O filesystem da função é efêmero; configure armazenamento persistente para anexos. Siga as variáveis e o callback descritos no README e em `INSTRUCOES_VERCEL.md`.

Após a publicação, valide os principais fluxos em um ambiente de teste. Habilite HTTPS, backups e revise privacidade, retenção de arquivos e os modelos de documentos antes de operar com dados reais. O repositório sozinho não hospeda o backend Flask.
