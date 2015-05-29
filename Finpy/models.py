from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core import validators
from django.contrib.auth.models import User

class UserProfile(models.Model):

    """Classe que representa o perfil de um usuario"""
    """In Portuguese: Perfil de Usuario"""

    # Usuario Associado
    user = models.OneToOneField(User)

    # Valores possiveis para Estado
    AC = 'AC'
    AL = 'AL'
    AP = 'AP'
    AM = 'AM'
    BA = 'BA'
    CE = 'CE'
    DF = 'DF'
    ES = 'ES'
    GO = 'GO'
    MA = 'MA'
    MT = 'MT'
    MS = 'MS'
    MG = 'MG'
    PA = 'PA'
    PB = 'PB'
    PR = 'PR'
    PE = 'PE'
    PI = 'PI'
    RJ = 'RJ'
    RN = 'RN'
    RS = 'RS'
    RO = 'RO'
    RR = 'RR'
    SC = 'SC'
    SP = 'SP'
    SE = 'SE'
    TO = 'TO'

    # Enum de Estados
    STATES = (
    (AC, 'AC'),
    (AL, 'AL'),
    (AP, 'AP'),
    (AM, 'AM'),
    (BA, 'BA'),
    (CE, 'CE'),
    (DF, 'DF'),
    (ES, 'ES'),
    (GO, 'GO'),
    (MA, 'MA'),
    (MT, 'MT'),
    (MS, 'MS'),
    (MG, 'MG'),
    (PA, 'PA'),
    (PB, 'PB'),
    (PR, 'PR'),
    (PE, 'PE'),
    (PI, 'PI'),
    (RJ, 'RJ'),
    (RN, 'RN'),
    (RS, 'RS'),
    (RO, 'RO'),
    (RR, 'RR'),
    (SC, 'SC'),
    (SP, 'SP'),
    (SE, 'SE'),
    (TO, 'TO')
    )
    
    # CPF
    cpf = models.CharField(_('cpf'),max_length=14,
        help_text=_('Use format ???.???.???-??'),
        validators=[
            validators.RegexValidator(r'^[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}$',_('Wrong Format!'), 'invalid'),
        ], blank=True)
    
    # Profissao
    job_title = models.CharField(_('Job Title'), max_length=150, blank=True)
    
    # Organizacao onde Trabalha
    organization = models.CharField(_('Organization'), max_length=150, blank=True)
    
    # Estado do Orgao Expedidor do RG
    expeditor_uf = models.CharField(_('Expeditor'),max_length=2, choices=STATES, default=DF, blank=True)
    
    # RG
    rg = models.CharField(_('rg'),max_length=9,
        help_text=_('Use format ?.???.???'),
        validators=[
                validators.RegexValidator(r'^[0-9]{1}\.?[0-9]{3}\.?[0-9]{3}$',_('Wrong Format!'), 'invalid'),
        ], blank=True)

    
    def __str__(self):
        return self.user.username

class Finance(models.Model):

    """Classe responsavel por armazenar lancamentos e simulacoes de investimento"""
    """In Portugues: Financa"""

    # Usuario Associado
    finance_user = models.OneToOneField(User)

    # Valor Total de Lancamentos
    total_entry_value = models.DecimalField(_('Total Entry Value'), decimal_places=2, max_digits=12)
    # Caixa Atual
    current_value = models.DecimalField(_('Current Entry Value'), decimal_places=2, max_digits=12)

    # Valores Possiveis de Periodicidade
    UNDEFINED = _('Undefined')
    DAILY = _('Daily') # Diario
    WEEKLY = _('Weekly') # Semanal
    MONTHLY = _('Monthly') # Mensal

    # Enum de Periodicidade
    PERIODICITY = (
    (UNDEFINED, _('Undefined')),
    (DAILY, _('Daily')),
    (WEEKLY, _('Weekly')),
    (MONTHLY, _('Monthly')),
    )

    def __str__(self):
        return self.currentValue

class InvestimentSimulation(models.Model):

    """Classe responsavel por manter simulacoes de investimento"""
    """In Portuguese: SimulacaoInvestimento"""

    # Valor presente do investimento
    present_value = models.DecimalField(_('Present Value'), decimal_places=2, max_digits=12, blank=True, null=True)

    # Valor futuro do investimento
    future_value = models.DecimalField(_('Future Value'), decimal_places=2, max_digits=12, blank=True, null=True)

    # Valor do pagamento utilizado na simulacao
    payment_value = models.DecimalField(_('Payment Value'), decimal_places=2, max_digits=12, blank=True, null=True)
 
    # Valor da taxa
    rate_value = models.DecimalField(_('Rate Value'), decimal_places=2, max_digits=3, blank=True, null=True)   
    
    # Tempo de duracao do investimento
    period_value = models.PositiveIntegerField(_('Period Value'), default=1, blank=True, null=True)

    # Itens do Enum
    FINANCIAL_MATH = _('Financial Math')
    INVESTMENT_RETURN = _('Investment Return')

    # Enum de Tipo de Simulacao
    SIMULATION_TYPE = (
    (FINANCIAL_MATH, _('Financial Math')),
    (INVESTMENT_RETURN, _('Investment Return')),
    )

    # Definicao do tipo de investimento
    simulation_type = models.CharField(_('Simulation Type'), choices=SIMULATION_TYPE, default=FINANCIAL_MATH, max_length=30)

    def __str__(self):
        return self.present_value

class SimulationAbstractStrategy:
    def calculate_investment(simulation_investment): pass

    def calculate_steps(simulation_investment): pass

    def validate_result(result): pass

class Category(models.Model):

    """Classe responsavel por registrar uma categoria de receita e despesa"""
    """Class responsible for registering the registry of revenues and expenses"""
    """In Portuguese: Categoria"""

    # Name of category recorded
    # Name of category never should be blank
    category_name = models.CharField(_('Name Category'), max_length=30, blank=False)

    # Detail of category recorded
    # Is not required
    category_description = models.TextField(_('Description Category'), max_length=150, blank=True)

    # Tipos de Lancamento
    INCOME = _('Income')
    EXPENSE = _('Expense')

    # Enum de Lancamentos
    ENTRY_TYPE = (
    (INCOME, _('Income')),
    (EXPENSE, _('Expense')),
    )

    def __str__(self):
        return self.category_name

class Entry(models.Model):

    """Classe responsavel por manter os dados em comuns de receitas e despesas"""
    """In Portuguese: Lancamento"""

    # Empresa/Organizacao/Entidade fonte da requisicao do Lancamento
    entry_source = models.CharField(_('Entry Source'), max_length=50, blank=True)

    # Registro do Valor do Lancamento
    entry_value = models.DecimalField(_('Entry Value'), decimal_places=2, max_digits=12)
    
    # Data de Vencimento
    entry_due_date = models.DateField(_('Due Date'))

    # Data de Registro do Lancamento
    entry_registration_date = models.DateField(_('Registration Date'))

    # Descricao do Lancamento
    entry_description = models.TextField(_('Entry Description'), max_length=150, blank=True)

    # Quantidade de Parcelas
    entry_quota_amount = models.PositiveIntegerField(_('Entry Quota Amount'), default=1)

    # Tipo de Periodicidade do Lancamento
    entry_periodicity = models.CharField(_('Entry Periodicity Type'), choices=Finance.PERIODICITY, default=Finance.MONTHLY, max_length=20)
    
    # Tipo do Lancamento
    entry_type = models.CharField(_('Entry Type'), choices=Category.ENTRY_TYPE, default=Category.EXPENSE, max_length=20)

    # Relacionamento de 1 pra n com Categoria de lancamento
    category = models.ForeignKey(Category, verbose_name=_('Entry Category'))

    # Relacionamento de 1 pra n com Usuario
    entry_user = models.ForeignKey(User, verbose_name=_('User'))

    # Valores Possiveis de Estado de Valor e Parcela
    OVERDUE = _('Overdue')
    NO_OVERDUE = _('No Overdue Yet')
    ALL_ENTRY = _('All Entry')

    # Enum de Estado de um Valor
    VALUE_STATE = (
        (OVERDUE, _('Overdue')),
        (NO_OVERDUE, _('No Overdue Yet')),
        (ALL_ENTRY, _('All Entry')),
    )

    # Enum de Estado de uma Parcela
    QUOTA_STATE = (
        (OVERDUE, _('Overdue')),
        (NO_OVERDUE, _('No Overdue Yet')),
    )

    def __str__(self):
        return self.entry_description