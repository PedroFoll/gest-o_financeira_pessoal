import os, re
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()
from django.test import Client
from pages.lancamentos.models import Lancamento

c = Client(enforce_csrf_checks=False)
# Pegar a lista como se fosse um browser
resp = c.get('/lancamentos/', HTTP_HOST='127.0.0.1')
html = resp.content.decode('utf-8')

# Buscar botões de excluir (data-action)
btns = re.findall(r'data-action="([^"]+)"', html)
print('data-action encontrados:', btns)

# Verificar o formExcluir
fidx = html.find('id="formExcluir"')
if fidx >= 0:
    print('\nformExcluir snippet:')
    print(html[fidx:fidx+300])
else:
    print('formExcluir NAO encontrado no HTML!')

# Verificar o script de JS
sidx = html.find('show.bs.modal')
if sidx >= 0:
    print('\nJS snippet:')
    print(html[sidx-50:sidx+300])
else:
    print('JS do modal NAO encontrado!')
