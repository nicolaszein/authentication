import abc


class BaseHandler(abc.ABC):

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass
