from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
from src.models import db, Hospede, Checkin

checkin_bp = Blueprint('checkin', __name__)

@checkin_bp.route('/novo-checkin')
def novo_checkin():
    """Página para criar um novo check-in"""
    return render_template('novo_checkin.html')

@checkin_bp.route('/checkins-ativos')
def checkins_ativos():
    """Página com lista de check-ins ativos"""
    checkins = Checkin.query.filter_by(status='Ativo').all()
    return render_template('checkins_ativos.html', checkins=checkins)

@checkin_bp.route('/historico')
def historico():
    """Página com histórico de check-ins finalizados"""
    # Parâmetros de filtro
    nome_filtro = request.args.get('nome', '')
    data_inicio = request.args.get('data_inicio', '')
    data_fim = request.args.get('data_fim', '')
    
    # Query base para check-ins finalizados
    query = Checkin.query.filter_by(status='Finalizado')
    
    # Aplicar filtros se fornecidos
    if nome_filtro:
        # Buscar por nome do hóspede principal
        query = query.join(Hospede).filter(
            Hospede.is_principal == True,
            Hospede.nome_completo.ilike(f'%{nome_filtro}%')
        )
    
    if data_inicio:
        try:
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            query = query.filter(Checkin.data_checkin >= data_inicio_obj)
        except ValueError:
            pass
    
    if data_fim:
        try:
            data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
            query = query.filter(Checkin.data_checkin <= data_fim_obj)
        except ValueError:
            pass
    
    checkins = query.order_by(Checkin.data_checkin.desc()).all()
    
    return render_template('historico.html', 
                         checkins=checkins,
                         nome_filtro=nome_filtro,
                         data_inicio=data_inicio,
                         data_fim=data_fim)

@checkin_bp.route('/checkin/<int:checkin_id>')
def detalhes_checkin(checkin_id):
    """Página com detalhes de um check-in específico"""
    checkin = Checkin.query.get_or_404(checkin_id)
    return render_template('detalhes_checkin.html', checkin=checkin)

@checkin_bp.route('/criar-checkin', methods=['POST'])
def criar_checkin():
    """Processa a criação de um novo check-in"""
    try:
        # Dados do check-in
        numero_apartamento = request.form.get('numero_apartamento')
        data_checkout_prevista_str = request.form.get('data_checkout_prevista')
        
        if not numero_apartamento or not data_checkout_prevista_str:
            flash('Número do apartamento e data de check-out prevista são obrigatórios', 'error')
            return redirect(url_for('checkin.novo_checkin'))
        
        # Converter data de checkout prevista
        try:
            data_checkout_prevista = datetime.strptime(data_checkout_prevista_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Data de check-out prevista inválida', 'error')
            return redirect(url_for('checkin.novo_checkin'))
        
        # Criar o check-in
        checkin = Checkin(
            numero_apartamento=numero_apartamento,
            data_checkout_prevista=data_checkout_prevista
        )
        db.session.add(checkin)
        db.session.flush()  # Para obter o ID do check-in
        
        # Processar hóspede principal
        hospede_principal = criar_hospede_from_form(request.form, checkin.id, is_principal=True)
        if not hospede_principal:
            db.session.rollback()
            flash('Erro ao processar dados do hóspede principal', 'error')
            return redirect(url_for('checkin.novo_checkin'))
        
        db.session.add(hospede_principal)
        
        # Processar acompanhantes (se houver)
        acompanhantes_data = extrair_acompanhantes_from_form(request.form)
        for acomp_data in acompanhantes_data:
            acompanhante = criar_hospede_from_dict(acomp_data, checkin.id, is_principal=False)
            if acompanhante:
                db.session.add(acompanhante)
        
        db.session.commit()
        flash('Check-in realizado com sucesso!', 'success')
        return redirect(url_for('checkin.checkins_ativos'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao realizar check-in: {str(e)}', 'error')
        return redirect(url_for('checkin.novo_checkin'))

@checkin_bp.route('/finalizar-checkin/<int:checkin_id>', methods=['POST'])
def finalizar_checkin(checkin_id):
    """Finaliza um check-in ativo"""
    try:
        checkin = Checkin.query.get_or_404(checkin_id)
        
        if checkin.status != 'Ativo':
            flash('Este check-in já foi finalizado', 'warning')
            return redirect(url_for('checkin.checkins_ativos'))
        
        checkin.finalizar_checkin()
        db.session.commit()
        
        flash('Check-out realizado com sucesso!', 'success')
        return redirect(url_for('checkin.checkins_ativos'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao finalizar check-in: {str(e)}', 'error')
        return redirect(url_for('checkin.checkins_ativos'))

def criar_hospede_from_form(form_data, checkin_id, is_principal=True):
    """Cria um objeto Hospede a partir dos dados do formulário"""
    try:
        # Campos obrigatórios
        nome_completo = form_data.get('nome_completo')
        data_nascimento_str = form_data.get('data_nascimento')
        documento = form_data.get('documento')
        orgao_expedidor = form_data.get('orgao_expedidor')  # Opcional
        uf_documento = form_data.get('uf_documento')  # Opcional
        cpf = form_data.get('cpf')  # Opcional
        ddd = form_data.get('ddd')  # Obrigatório
        telefone = form_data.get('telefone')
        email = form_data.get('email')  # Opcional
        
        if not all([nome_completo, data_nascimento_str, documento, ddd, telefone]):
            return None
        
        # Converter data de nascimento
        data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
        idade = Hospede.calcular_idade(data_nascimento)
        
        # Campos opcionais (não obrigatórios para nenhum tipo de hóspede)
        endereco = form_data.get('endereco')
        cep = form_data.get('cep')
        cidade = form_data.get('cidade')
        estado = form_data.get('estado')
        pais = form_data.get('pais')
        observacoes = form_data.get('observacoes')
        
        hospede = Hospede(
            nome_completo=nome_completo,
            data_nascimento=data_nascimento,
            idade=idade,
            documento=documento,
            orgao_expedidor=orgao_expedidor,
            uf_documento=uf_documento,
            cpf=cpf,
            endereco=endereco,
            cep=cep,
            cidade=cidade,
            estado=estado,
            pais=pais,
            ddd=ddd,
            telefone=telefone,
            email=email,
            observacoes=observacoes,
            is_principal=is_principal,
            checkin_id=checkin_id
        )
        
        return hospede
        
    except Exception as e:
        print(f"Erro ao criar hóspede: {e}")
        return None

def criar_hospede_from_dict(data, checkin_id, is_principal=False):
    """Cria um objeto Hospede a partir de um dicionário de dados"""
    try:
        # Converter data de nascimento
        data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        idade = Hospede.calcular_idade(data_nascimento)
        
        hospede = Hospede(
            nome_completo=data['nome_completo'],
            data_nascimento=data_nascimento,
            idade=idade,
            documento=data['documento'],
            orgao_expedidor=data.get('orgao_expedidor'),
            uf_documento=data.get('uf_documento'),
            cpf=data.get('cpf'),
            ddd=data['ddd'],
            telefone=data['telefone'],
            email=data.get('email'),
            observacoes=data.get('observacoes'),
            is_principal=is_principal,
            checkin_id=checkin_id
        )
        
        return hospede
        
    except Exception as e:
        print(f"Erro ao criar acompanhante: {e}")
        return None

def extrair_acompanhantes_from_form(form_data):
    """Extrai dados dos acompanhantes do formulário"""
    acompanhantes = []
    i = 0
    
    while True:
        nome_key = f'acompanhante_{i}_nome_completo'
        if nome_key not in form_data or not form_data.get(nome_key):
            break
        
        acompanhante_data = {
            'nome_completo': form_data.get(f'acompanhante_{i}_nome_completo'),
            'data_nascimento': form_data.get(f'acompanhante_{i}_data_nascimento'),
            'documento': form_data.get(f'acompanhante_{i}_documento'),
            'orgao_expedidor': form_data.get(f'acompanhante_{i}_orgao_expedidor'),
            'uf_documento': form_data.get(f'acompanhante_{i}_uf_documento'),
            'cpf': form_data.get(f'acompanhante_{i}_cpf'),
            'ddd': form_data.get(f'acompanhante_{i}_ddd'),
            'telefone': form_data.get(f'acompanhante_{i}_telefone'),
            'email': form_data.get(f'acompanhante_{i}_email'),
            'observacoes': form_data.get(f'acompanhante_{i}_observacoes')
        }
        
        # Verificar se todos os campos obrigatórios estão preenchidos
        if all([acompanhante_data['nome_completo'], 
                acompanhante_data['data_nascimento'],
                acompanhante_data['documento']]):
            acompanhantes.append(acompanhante_data)
        
        i += 1
    
    return acompanhantes



from src.utils.country_codes import COUNTRY_CODES

def get_country_code_from_country(pais):
    """Retorna o código do país com base no nome do país."""
    if not pais:
        return ""
    return COUNTRY_CODES.get(pais.lower(), "")  # Retorna string vazia se não encontrar

