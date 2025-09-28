from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class Checkin(db.Model):
    __tablename__ = 'checkins'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_apartamento = db.Column(db.String(10), nullable=False)
    data_checkin = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_checkout_prevista = db.Column(db.Date, nullable=False)  # Data prevista para checkout
    data_checkout = db.Column(db.DateTime, nullable=True)  # Nula para check-ins ativos
    status = db.Column(db.String(20), nullable=False, default='Ativo')  # Ativo ou Finalizado
    
    # Relacionamento com hóspedes
    hospedes = db.relationship('Hospede', backref='checkin', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Checkin Apt {self.numero_apartamento} - {self.status}>'
    
    @property
    def hospede_principal(self):
        """Retorna o hóspede principal deste check-in"""
        for hospede in self.hospedes:
            if hospede.is_principal:
                return hospede
        return None
    
    @property
    def acompanhantes(self):
        """Retorna a lista de acompanhantes deste check-in"""
        return [hospede for hospede in self.hospedes if not hospede.is_principal]
    
    @property
    def total_hospedes(self):
        """Retorna o número total de hóspedes"""
        return len(self.hospedes)
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'numero_apartamento': self.numero_apartamento,
            'data_checkin': self.data_checkin.strftime('%Y-%m-%d %H:%M:%S') if self.data_checkin else None,
            'data_checkout_prevista': self.data_checkout_prevista.strftime('%Y-%m-%d') if self.data_checkout_prevista else None,
            'data_checkout': self.data_checkout.strftime('%Y-%m-%d %H:%M:%S') if self.data_checkout else None,
            'status': self.status,
            'hospede_principal': self.hospede_principal.to_dict() if self.hospede_principal else None,
            'acompanhantes': [acomp.to_dict() for acomp in self.acompanhantes],
            'total_hospedes': self.total_hospedes
        }
    
    def finalizar_checkin(self):
        """Finaliza o check-in definindo a data de checkout e status"""
        self.data_checkout = datetime.utcnow()
        self.status = 'Finalizado'


class Hospede(db.Model):
    __tablename__ = 'hospedes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(200), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    documento = db.Column(db.String(50), nullable=False)
    orgao_expedidor = db.Column(db.String(50), nullable=True)  # Órgão expedidor do documento
    uf_documento = db.Column(db.String(2), nullable=True)  # UF do documento
    cpf = db.Column(db.String(14), nullable=True)  # Formato: 000.000.000-00 (opcional)
    
    # Campos opcionais para acompanhantes (obrigatórios para hóspede principal)
    endereco = db.Column(db.String(200), nullable=True)
    cep = db.Column(db.String(20), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(100), nullable=True)
    pais = db.Column(db.String(100), nullable=True)
    
    ddd = db.Column(db.String(2), nullable=False)  # DDD obrigatório
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=True)  # E-mail opcional
    observacoes = db.Column(db.Text, nullable=True)
    
    # Indica se é o hóspede principal ou acompanhante
    is_principal = db.Column(db.Boolean, nullable=False, default=False)
    
    # Relacionamento com check-in
    checkin_id = db.Column(db.Integer, db.ForeignKey('checkins.id'), nullable=False)
    
    def __repr__(self):
        return f'<Hospede {self.nome_completo}>'
    
    @staticmethod
    def calcular_idade(data_nascimento):
        """Calcula a idade baseada na data de nascimento"""
        hoje = date.today()
        idade = hoje.year - data_nascimento.year
        
        # Verifica se já fez aniversário este ano
        if hoje.month < data_nascimento.month or (hoje.month == data_nascimento.month and hoje.day < data_nascimento.day):
            idade -= 1
            
        return idade
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome_completo': self.nome_completo,
            'data_nascimento': self.data_nascimento.strftime('%Y-%m-%d') if self.data_nascimento else None,
            'idade': self.idade,
            'documento': self.documento,
            'orgao_expedidor': self.orgao_expedidor,
            'uf_documento': self.uf_documento,
            'cpf': self.cpf,
            'endereco': self.endereco,
            'cep': self.cep,
            'cidade': self.cidade,
            'estado': self.estado,
            'pais': self.pais,
            'ddd': self.ddd,
            'telefone': self.telefone,
            'email': self.email,
            'observacoes': self.observacoes,
            'is_principal': self.is_principal,
            'checkin_id': self.checkin_id
        }

