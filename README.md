Sistema de Gestão de Check-in/Check-out

Um sistema completo para gestão de hospedagem em hotéis, desenvolvido com Flask e Jinja2, com interface moderna baseada em cartões e funcionalidades avançadas.

## 🚀 Características

### Funcionalidades Principais
- **Check-in de Hóspedes**: Registro completo de hóspedes com dados pessoais e de contato
- **Gestão de Acompanhantes**: Suporte para múltiplos hóspedes por apartamento
- **Cálculo Automático de Idade**: Baseado na data de nascimento
- **Check-ins Ativos**: Visualização e gestão de hospedagens em andamento
- **Histórico Completo**: Consulta de check-ins finalizados com filtros avançados
- **Interface Responsiva**: Design moderno que funciona em desktop e mobile

### Tecnologias Utilizadas
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Template Engine**: Jinja2
- **Banco de Dados**: SQLite
- **ORM**: SQLAlchemy
- **Icons**: Bootstrap Icons
- **Fonts**: Google Fonts (Inter)

## 📋 Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

## 🛠️ Instalação e Configuração

### 1. Clone ou extraia o projeto
```bash
# Se você recebeu o projeto como arquivo ZIP, extraia-o
# Se está clonando de um repositório:
git clone <url-do-repositorio>
cd hotel-checkin-system
```

### 2. Ative o ambiente virtual
```bash
# No Linux/Mac:
source venv/bin/activate

# No Windows:
venv\\Scripts\\activate
```

### 3. Instale as dependências (se necessário)
```bash
pip install -r requirements.txt
```

### 4. Execute o sistema
```bash
python src/main.py
```

### 5. Acesse o sistema
Abra seu navegador e acesse: `http://localhost:5000`

## 📱 Como Usar

### Dashboard Principal
- Acesse a página inicial para uma visão geral do sistema
- Use os cartões para navegar rapidamente entre as funcionalidades

### Novo Check-in
1. Clique em "Novo Check-in" no menu lateral ou dashboard
2. Preencha os dados do apartamento
3. Complete as informações do hóspede principal:
   - Nome completo, data de nascimento (idade calculada automaticamente)
   - Documento, nacionalidade, profissão
   - Endereço completo, telefone, e-mail
   - Observações (opcional)
4. Adicione acompanhantes clicando no botão "+" (opcional)
5. Clique em "Realizar Check-in"

### Check-ins Ativos
- Visualize todos os apartamentos ocupados
- Veja informações resumidas de cada hospedagem
- Clique em "Ver Detalhes" para informações completas
- Use "Check-out" para finalizar uma hospedagem

### Histórico
- Consulte check-ins finalizados
- Use filtros por nome do hóspede ou período
- Clique em qualquer cartão para ver detalhes completos

## 🗂️ Estrutura do Projeto

```
hotel-checkin-system/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py          # Modelos de dados (Checkin, Hospede)
│   ├── routes/
│   │   └── checkin.py         # Rotas do sistema
│   ├── templates/
│   │   ├── base.html          # Template base
│   │   ├── index.html         # Dashboard
│   │   ├── novo_checkin.html  # Formulário de check-in
│   │   ├── checkins_ativos.html
│   │   ├── detalhes_checkin.html
│   │   └── historico.html
│   ├── database/
│   │   └── app.db            # Banco de dados SQLite
│   └── main.py               # Aplicação principal
├── venv/                     # Ambiente virtual Python
├── requirements.txt          # Dependências
└── README.md                # Esta documentação
```

## 💾 Banco de Dados

O sistema utiliza SQLite com duas tabelas principais:

### Tabela `checkins`
- `id`: Identificador único
- `numero_apartamento`: Número do apartamento
- `data_checkin`: Data e hora do check-in
- `data_checkout`: Data e hora do check-out (nulo para ativos)
- `status`: Status (Ativo/Finalizado)

### Tabela `hospedes`
- `id`: Identificador único
- `nome_completo`: Nome completo do hóspede
- `data_nascimento`: Data de nascimento
- `idade`: Idade calculada automaticamente
- `documento`: RG/CPF/Passaporte
- `nacionalidade`: Nacionalidade
- `profissao`: Profissão
- `endereco`, `cep`, `cidade`, `estado`, `pais`: Endereço (opcional para acompanhantes)
- `telefone`: Telefone de contato
- `email`: E-mail de contato
- `observacoes`: Observações adicionais
- `is_principal`: Indica se é hóspede principal
- `checkin_id`: Referência ao check-in

## 🎨 Interface

### Design Moderno
- Sidebar com navegação intuitiva
- Cartões com hover effects e animações
- Cores e tipografia profissionais
- Layout responsivo para todos os dispositivos

### Funcionalidades JavaScript
- Cálculo automático de idade
- Adição/remoção dinâmica de acompanhantes
- Validação de formulários
- Animações e transições suaves

## 🔧 Personalização

### Cores e Estilos
As variáveis CSS estão definidas no arquivo `base.html`:
```css
:root {
    --primary-color: #2563eb;
    --primary-dark: #1d4ed8;
    --secondary-color: #64748b;
    /* ... outras variáveis */
}
```

### Adicionando Novos Campos
1. Modifique os modelos em `src/models/models.py`
2. Atualize os formulários nos templates
3. Ajuste as rotas em `src/routes/checkin.py`

## 🚀 Deployment

### Desenvolvimento Local
O sistema já está configurado para execução local com Flask development server.

### Produção
Para ambiente de produção, considere:
- Usar um servidor WSGI como Gunicorn
- Configurar um banco de dados mais robusto (PostgreSQL, MySQL)
- Implementar HTTPS
- Configurar backup automático do banco de dados

## 📝 Licença

Este projeto foi desenvolvido para uso interno. Todos os direitos reservados.

## 🆘 Suporte

Para dúvidas ou problemas:
1. Verifique se todas as dependências estão instaladas
2. Confirme que o Python 3.11+ está sendo usado
3. Verifique se a porta 5000 não está sendo usada por outro processo

## 📈 Futuras Melhorias

- Botao para editar o check-in,
- filtro por apartamento no historico,
- ddd+telefone juntos no mesmo campo,
- Lista que autocompleta os paises para determinar o codigo de país
- Sistema de autenticação e usuários
- Relatórios em PDF
- Integração com sistemas de pagamento
- API REST para integração com outros sistemas
- Dashboard com gráficos e estatísticas
- Sistema de notificações
- Backup automático

