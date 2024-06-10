from datetime import datetime

class Usuario:
    """
    Classe usuário no sistema.

    Atributos:
        id (int): ID do usuário.
        nome (str): Nome do usuário.
        tipo (str): Tipo do usuário ('maqueiro' ou 'administrador').
    """
    def __init__(self, id, nome, tipo):
        self._id = id
        self._nome = nome
        self._tipo = tipo  # 'maqueiro' ou 'administrador'

    @property
    def id(self):
        """int: Retorna o ID do usuário."""
        return self._id

    @property
    def nome(self):
        """str: Retorna o nome do usuário."""
        return self._nome

    @property
    def tipo(self):
        """str: Retorna o tipo do usuário ('maqueiro' ou 'administrador')."""
        return self._tipo

    @id.setter
    def id(self, id):
        self._id = id

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @tipo.setter
    def tipo(self, tipo):
        self._tipo = tipo

class Paciente:
    """
    Classe paciente no sistema.

    Atributos:
        id (int): ID do paciente.
        nome (str): Nome do paciente.
        cpf (str): CPF do paciente.
        localizacao (str): Localização do paciente.
        condicao (str): Condição do paciente.
        transporte (str): Status de transporte do paciente.
        urgencia (str): Nível de urgência do paciente.
    """
    def __init__(self, nome, cpf, localizacao, condicao, transporte, urgencia=None):
        self._id = None
        self._nome = nome
        self._cpf = cpf
        self._localizacao = localizacao
        self._condicao = condicao
        self._transporte = transporte
        self._urgencia = urgencia

    @property
    def id(self):
        """int: Retorna o ID do paciente."""
        return self._id

    @property
    def nome(self):
        """str: Retorna o nome do paciente."""
        return self._nome

    @property
    def cpf(self):
        """str: Retorna o CPF do paciente."""
        return self._cpf

    @property
    def localizacao(self):
        """str: Retorna a localização do paciente."""
        return self._localizacao

    @property
    def condicao(self):
        """str: Retorna a condição do paciente."""
        return self._condicao

    @property
    def transporte(self):
        """str: Retorna o status de transporte do paciente."""
        return self._transporte

    @property
    def urgencia(self):
        """str: Retorna o nível de urgência do paciente."""
        return self._urgencia

    @id.setter
    def id(self, id):
        self._id = id

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @cpf.setter
    def cpf(self, cpf):
        self._cpf = cpf

    @localizacao.setter
    def localizacao(self, localizacao):
        self._localizacao = localizacao

    @condicao.setter
    def condicao(self, condicao):
        self._condicao = condicao

    @transporte.setter
    def transporte(self, transporte):
        self._transporte = transporte

    @urgencia.setter
    def urgencia(self, urgencia):
        self._urgencia = urgencia

    def definir_id(self, id):
        """Define o ID do paciente."""
        self.id = id

    def atualizar_condicao(self, nova_condicao):
        """Atualiza a condição do paciente."""
        self.condicao = nova_condicao

    def iniciar_transporte(self):
        """Inicia o transporte do paciente."""
        self.transporte = 'Em transporte'
        self._inicio_transporte = datetime.now()

    def finalizar_transporte(self):
        """Finaliza o transporte do paciente."""
        self.transporte = 'Chegou ao destino'

class Maqueiro(Usuario):
    """
    Classe maqueiro, que é um usuário.

    Atributos:
        coren (str): COREN do maqueiro.
        data_nascimento (str): Data de nascimento do maqueiro.
        sexo (str): Sexo do maqueiro.
        tarefas (list): Lista de tarefas atribuídas ao maqueiro.
    """
    def __init__(self, id, nome, coren, data_nascimento, sexo):
        super().__init__(id, nome, 'maqueiro')
        self._coren = coren
        self._data_nascimento = data_nascimento
        self._sexo = sexo
        self._login = None
        self._senha = None
        self._tarefas = []

    @property
    def coren(self):
        """str: Retorna o COREN do maqueiro."""
        return self._coren

    @property
    def data_nascimento(self):
        """str: Retorna a data de nascimento do maqueiro."""
        return self._data_nascimento

    @property
    def sexo(self):
        """str: Retorna o sexo do maqueiro."""
        return self._sexo

    @property
    def tarefas(self):
        """list: Retorna a lista de tarefas atribuídas ao maqueiro."""
        return self._tarefas

    @coren.setter
    def coren(self, coren):
        self._coren = coren

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento):
        self._data_nascimento = data_nascimento

    @sexo.setter
    def sexo(self, sexo):
        self._sexo = sexo

    def adicionar_tarefa(self, tarefa):
        """Adiciona uma tarefa à lista de tarefas do maqueiro."""
        self.tarefas.append(tarefa)

class Tarefa:
    """
    Classe tarefa no sistema.

    Atributos:
        id (int): ID da tarefa.
        descricao (str): Descrição da tarefa.
        prioridade (str): Prioridade da tarefa.
        status (str): Status da tarefa.
        paciente (Paciente): Paciente relacionado à tarefa.
        localizacao (str): Localização da tarefa.
        maqueiro (Maqueiro): Maqueiro atribuído à tarefa.
    """
    def __init__(self, id, descricao, prioridade, paciente, localizacao, maqueiro):
        self._id = id
        self._descricao = descricao
        self._prioridade = prioridade
        self._status = 'pendente'
        self._paciente = paciente
        self._localizacao = localizacao
        self._maqueiro = maqueiro

    @property
    def id(self):
        """int: Retorna o ID da tarefa."""
        return self._id

    @property
    def descricao(self):
        """str: Retorna a descrição da tarefa."""
        return self._descricao

    @property
    def prioridade(self):
        """str: Retorna a prioridade da tarefa."""
        return self._prioridade

    @property
    def status(self):
        """str: Retorna o status da tarefa."""
        return self._status

    @property
    def paciente(self):
        """Paciente: Retorna o paciente relacionado à tarefa."""
        return self._paciente

    @property
    def localizacao(self):
        """str: Retorna a localização da tarefa."""
        return self._localizacao

    @property
    def maqueiro(self):
        """Maqueiro: Retorna o maqueiro atribuído à tarefa."""
        return self._maqueiro

    @id.setter
    def id(self, id):
        self._id = id

    @descricao.setter
    def descricao(self, descricao):
        self._descricao = descricao

    @prioridade.setter
    def prioridade(self, prioridade):
        self._prioridade = prioridade

    @status.setter
    def status(self, status):
        self._status = status

    @paciente.setter
    def paciente(self, paciente):
        self._paciente = paciente

    @localizacao.setter
    def localizacao(self, localizacao):
        self._localizacao = localizacao

    @maqueiro.setter
    def maqueiro(self, maqueiro):
        self._maqueiro = maqueiro

class Incidente:
    """
    Classe incidente no sistema.

    Atributos:
        id (int): ID do incidente.
        descricao (str): Descrição do incidente.
        maqueiro (Maqueiro): Maqueiro envolvido no incidente.
        paciente (Paciente): Paciente relacionado ao incidente.
        data_hora (str): Data e hora do incidente.
        status (str): Status do incidente.
    """
    def __init__(self, id, descricao, maqueiro, paciente, data_hora):
        self._id = id
        self._descricao = descricao
        self._maqueiro = maqueiro
        self._paciente = paciente
        self._data_hora = data_hora
        self._status = 'pendente'

    @property
    def id(self):
        """int: Retorna o ID do incidente."""
        return self._id

    @property
    def descricao(self):
        """str: Retorna a descrição do incidente."""
        return self._descricao

    @property
    def maqueiro(self):
        """Maqueiro: Retorna o maqueiro envolvido no incidente."""
        return self._maqueiro

    @property
    def paciente(self):
        """Paciente: Retorna o paciente relacionado ao incidente."""
        return self._paciente

    @property
    def data_hora(self):
        """str: Retorna a data e hora do incidente."""
        return self._data_hora

    @property
    def status(self):
        """str: Retorna o status do incidente."""
        return self._status

    @id.setter
    def id(self, id):
        self._id = id

    @descricao.setter
    def descricao(self, descricao):
        self._descricao = descricao

    @maqueiro.setter
    def maqueiro(self, maqueiro):
        self._maqueiro = maqueiro

    @paciente.setter
    def paciente(self, paciente):
        self._paciente = paciente

    @data_hora.setter
    def data_hora(self, data_hora):
        self._data_hora = data_hora

    @status.setter
    def status(self, status):
        self._status = status

class SolicitacaoTransporte:
    """
    Classe solicitação de transporte no sistema.

    Atributos:
        id (int): ID da solicitação de transporte.
        descricao (str): Descrição da solicitação de transporte.
        paciente (Paciente): Paciente relacionado à solicitação.
        data_hora (str): Data e hora da solicitação.
        maqueiro (Maqueiro): Maqueiro atribuído à solicitação.
        status (str): Status da solicitação.
    """
    def __init__(self, id, descricao, paciente, data_hora, maqueiro):
        self._id = id
        self._descricao = descricao
        self._paciente = paciente
        self._data_hora = data_hora
        self._maqueiro = maqueiro
        self._status = 'pendente'

    @property
    def id(self):
        """int: Retorna o ID da solicitação de transporte."""
        return self._id

    @property
    def descricao(self):
        """str: Retorna a descrição da solicitação de transporte."""
        return self._descricao

    @property
    def paciente(self):
        """Paciente: Retorna o paciente relacionado à solicitação."""
        return self._paciente

    @property
    def data_hora(self):
        """str: Retorna a data e hora da solicitação."""
        return self._data_hora

    @property
    def maqueiro(self):
        """Maqueiro: Retorna o maqueiro atribuído à solicitação."""
        return self._maqueiro

    @property
    def status(self):
        """str: Retorna o status da solicitação de transporte."""
        return self._status

    @id.setter
    def id(self, id):
        self._id = id

    @descricao.setter
    def descricao(self, descricao):
        self._descricao = descricao

    @paciente.setter
    def paciente(self, paciente):
        self._paciente = paciente

    @data_hora.setter
    def data_hora(self, data_hora):
        self._data_hora = data_hora

    @maqueiro.setter
    def maqueiro(self, maqueiro):
        self._maqueiro = maqueiro

    @status.setter
    def status(self, status):
        self._status = status