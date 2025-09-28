from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Checkin(db.Model):
    __tablename__ = 'checkins'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_apartamento = db.Column(db.String(10), nullable=False)
    data_checkin = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
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

