import os

os.makedirs('.streamlit', exist_ok=True)
with open('.streamlit/config.toml', 'w', encoding='utf-8') as f:
    f.write('[server]\nheadless = true\n')

if os.path.exists('app.py'):
    with open('app.py', 'rb') as f:
        c = f.read().decode('utf-8', errors='ignore')
    
    repls = {'Ã¡':'á','Ã ':'à','Ã¢':'â','Ã£':'ã','Ã©':'é','Ãª':'ê','Ã\xad':'í','Ã³':'ó','Ã´':'ô','Ãµ':'õ','Ãº':'ú','Ã§':'ç','Â':'','â€”':'—','âš ï¸':'⚠️','ðŸ«':'🏫','ðŸ“Š':'📊','ðŸ“':'📝','ðŸ‘‡':'👇'}
    for k, v in repls.items():
        c = c.replace(k, v)
        
    if not c.startswith('# -*- coding: utf-8 -*-'):
        c = '# -*- coding: utf-8 -*-\n' + c
        
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Sucesso!")
else:
    print("⚠️ app.py nao encontrado!")
