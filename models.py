# (david neves)
# lembrando q uma class é a definição ou o modelo de como algo vai ser e nao um objeto tlgd
# hierarquia: criar primeiro as classes que nao dependem de ninguem, entao category e user vem antes de task



#Yara aquando tu tiver dzd isso nao esquece daquilo 


# ─────────────────────────────────────────────
# CLASS CATEGORY
# representa o tipo/categoria da tarefa (ex: trabalho, estudo, pessoal)
# nao depende de nenhuma outra classe, entao vem primeira
# ─────────────────────────────────────────────
class Category:

    # toda vez q cria um objeto novo esse metodo é rodado automaticamente
    # ex: categoria = Category(1, "trabalho") → o __init__ é chamado na hora pegando o 1 como id e "trabalho" como name
    # __init__ é uma convencao do python, significa inicializar, o py reconhece esse nome e sabe q deve rodar ele automaticamente quando um objeto é criado
    # os __ no __init__ identificam que é um metodo magico do python (dunder method)
    # o str e o int nao precisaria maaaaas deixa o codigo mais claro hehe
    def __init__(self, id: int, name: str):

        # self representa ele mesmo, o proprio objeto que esta sendo criado
        # é extremamente importante pois garante que o id vai pro id dele mesmo e o name vai pro name dele mesmo
        # lembrar: se for querer usar em outro metodo entao usa self, se nao, nao precisa (dentro do método tô falando, no parametro SEMPRE tem)
        # self.__id é diferente de self.id (sem __)
        # as underlines duplas tornam o atributo privado, foca em segurança
        # ninguem de fora consegue acessar diretamente, so atraves dos getters
        self.__id = id
        self.__name = name

    # get_id e get_name sao os getters
    # lembra q o id e o name estao como privados por conta dos __?
    # ninguem de fora da class consegue acessar eles diretamente
    # mas em algum momento vai ter q pegar esses valores, tipo quando o karlos for listar as categorias
    # o getter existe pra isso: ser a unica forma controlada de acessar um dado privado
    # ex: categoria.get_id() → retorna o id daquela categoria
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    # to_dict significa "to dictionary" → converter para dicionario
    # quando a API responder uma requisicao ela precisa mandar os dados em formato JSON
    # o flask nao consegue pegar o objeto category e converter sozinho, ele nao sabe nem oq é isso
    # com o to_dict transformamos o objeto num dicionario que o flask consegue converter pra JSON na hora
    # ex: {"id": 1, "name": "Trabalho"} → isso é o JSON que o postman/navegador vai receber
    def to_dict(self):
        return {
            "id": self.__id,
            "name": self.__name
        }


# ─────────────────────────────────────────────
# CLASS USER
# representa o responsavel pela tarefa
# nao depende de nenhuma outra classe, entao vem antes da task
# ─────────────────────────────────────────────
class User:

    # mesma logica do category, so q agora com 3 atributos: id, name e email
    def __init__(self, id: int, name: str, email: str):
        self.__id = id
        self.__name = name
        self.__email = email

    # getters do user, mesma logica do category
    # quem precisar do nome ou email do usuario vai usar esses metodos
    # ex: user.get_email() → retorna o email daquele usuario
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    # mesma logica do category, converte o objeto user pra dicionario
    # assim o flask consegue transformar em JSON e mandar na resposta da API
    def to_dict(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "email": self.__email
        }


# ─────────────────────────────────────────────
# CLASS TASK
# representa a tarefa em si, é a classe principal do projeto
# depende de User e Category, entao vem por ultimo (hierarquia)
# ─────────────────────────────────────────────
class Task:

    # task tem 8 atributos, os 2 ultimos (user e category) sao objetos de outras classes
    # isso é o relacionamento entre classes que o professor pediu
    # deadline é str pq data geralmente vem assim: "30/04/2026", int nao faria sentido
    def __init__(self, id: int, title: str, description: str, status: str, priority: str, deadline: str, user: User, category: Category):
        self.__id = id
        self.__title = title
        self.__description = description
        self.__status = status        # pending, doing, done
        self.__priority = priority    # low, medium, high
        self.__deadline = deadline    # ex: "30/04/2026"
        self.__user = user            # objeto User completo
        self.__category = category    # objeto Category completo

    # getters da task, mesma logica das outras classes
    def get_id(self):
        return self.__id

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

    def get_status(self):
        return self.__status

    def get_priority(self):
        return self.__priority

    def get_deadline(self):
        return self.__deadline

    def get_user(self):
        return self.__user

    def get_category(self):
        return self.__category

    # to_dict da task tem uma diferenca importante em relacao aos outros
    # user e category sao objetos, nao valores simples como string ou int
    # o flask nao consegue converter objetos diretamente pra JSON
    # entao chamamos o .to_dict() do user e do category tambem
    # assim tudo vira dicionario no final e o flask consegue converter tudo pra JSON certinho
    def to_dict(self):
        return {
            "id": self.__id,
            "title": self.__title,
            "description": self.__description,
            "status": self.__status,
            "priority": self.__priority,
            "deadline": self.__deadline,
            "user": self.__user.to_dict(),        # chama o to_dict do objeto User
            "category": self.__category.to_dict() # chama o to_dict do objeto Category
        }