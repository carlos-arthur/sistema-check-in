from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class Hospede(db.Model):
    __tablename__ = 'hospedes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(200), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    documento = db.Column(db.String(50), nullable=False)
    profissao = db.Column(db.String(100), nullable=False)
    
    # Campos opcionais para acompanhantes (obrigatórios para hóspede principal)
    endereco = db.Column(db.String(200), nullable=True)
    cep = db.Column(db.String(20), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(100), nullable=True)
    pais = db.Column(db.String(100), nullable=True)
    
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
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
            'profissao': self.profissao,
            'endereco': self.endereco,
            'cep': self.cep,
            'cidade': self.cidade,
            'estado': self.estado,
            'pais': self.pais,
            'telefone': self.telefone,
            'email': self.email,
            'observacoes': self.observacoes,
            'is_principal': self.is_principal,
            'checkin_id': self.checkin_id
        }

