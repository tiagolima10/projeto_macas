class SistemaDeNotificacoes:
    """
    Classe que gerencia o sistema de notificações.

    Attributes:
        _notificacoes (list): Lista de notificações armazenadas no sistema.
    """

    def __init__(self):
        """
        Inicializa uma nova instância do sistema de notificações.
        """
        self._notificacoes = []

    def adicionar_notificacao(self, notificacao):
        """
        Adiciona uma nova notificação ao sistema.

        Args:
            notificacao (str): A notificação a ser adicionada.
        """
        self._notificacoes.append(notificacao)

    def get_notificacoes(self):
        """
        Retorna a lista de notificações armazenadas no sistema.

        Returns:
            list: Lista de notificações.
        """
        return self._notificacoes

    def remover_notificacao(self, notificacao):
        """
        Remove uma notificação específica do sistema, se existir.

        Args:
            notificacao (str): A notificação a ser removida.
        """
        if notificacao in self._notificacoes:
            self._notificacoes.remove(notificacao)
