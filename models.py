                    #(david neves) tinha esquecido da hierarquia do que criar primeiro classe que não depende de ninguém logo, lembrando q uma class é a definicação ou o
                        # modelo de como algo vai ser e nao um objeto tlgd
class Category:
    def __init__(self, id: int, name:str):
        self.__id = id
        self.__name = name

        #def __init__(self, id: int, name:str): toda vez q cria um objeto novo esse modelo/metodo é rodado, entao quando cria algum vai ser tipo
        #categoria = Category(1, "trabalho") ai tipo o __init__  (init é uma conversão do python, siginifica inicializar o python reconhece esse nome e sabe q deve rodar ele automaticamente quadno um objeto é criado,) é chamado na hora pegando o 1 como id e "trabalho" como name
        #os unerline (__ __) no parametro do init sao para identificar que é um metodo magico de pthon, ja nos atributos  omo self.__id que sao para encapsulamento

        #o self representa ele mesmo o proprio objeto que esta sendo criado, é extremanente importante pois garante que o id para vai o id dele mesmo e o name vai para ele mesmo, mas lembrar de que se for querer chamar em outro metodo entao usa self, se nao, nao precisa do self (dentro do método estou falando, no parametro SEMPRE tem)

        #o str e o int nao precisaria maaaaas deixa o codigo mais claro hehe

        #self.__id = id, presta atencao, self.__nome = nome é diferente de self.nome = nome ( o que ja vimos antes nas aulas do prof), essas underline duplas tornam o atributo privadoe, ele foca em segurança, tipo so vai da pra modificar o objeto com o update_status,pq alguem mexeria no de outra pessoa? slaa

    def get_id(self):
        return self.__id
    
        #criando um metodo chamado get_id (pegar id), lembra q o id  e o name estao como privados agora por conta dos __? ninguem de fora da class consegfue acessar ekles, mas em algum momento vai ter q pegar os vlores pra exibir as categorias talvez e o getter existe pra isso, ser a punica forma controlada de acessar um dado privado. tipo quando o karlos for fazer o endpont de listar categorias, ele vai precisar do id e do nome, ele vai usar o categoria.get_id() 

    def get_name(self):
        return self.__name
    
        #mesma coisa vou repetir nn

    def to_dict(self):
        return {
            "id": self.__id,
            "name": self.__name
            
            #o to  dict (to dictionary) é para converter para dicionario mesmo, pq? quando a API reponder uma requisdição ela precisa mandar os dados em formato JSON lembra ai sim q o navegador e opostman entendem o flask nao consegue pegar o objeto category e converter sozinho el enao sabe nem oq e isso na real, ja com o to dict transforma o objeto num dicionario que o flask consegue conerverter tipo "id": 1, "name": "Trabalho"
        }


