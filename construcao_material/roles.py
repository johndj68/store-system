from rolepermissions.roles import AbstractUserRole

class Gerente(AbstractUserRole):
    available_permissions = {
        'cadastra_produto' : True,
        'liberar_descontos' : True,
        'cadastrar_vendedor': True,
    }

class Vendedor(AbstractUserRole):
    available_permissions = {
        'realisar_venda' : True,
    }