from requests import get
from bs4 import BeautifulSoup


delimiter = '_______________________________________________________________________________\n'


def get_spells_from_site(site):
    page = get(site)
    soup = BeautifulSoup(page.content.decode(), 'html.parser')
    main_div = soup.find('div', {'role': 'main'})
    spells = main_div.find_all('a')
    with open('all_spells.txt', 'w') as f:
        for spell in spells:
            s = BeautifulSoup(get(site + spell.attrs['href']).content.decode(), 'html.parser')
            f.write(str(s.find('div', {'role': 'main'})))
            f.write('\n' + delimiter)


def get_tags():
    with open('all_spells.txt', 'r') as f:
        tags = set()
        for page in f.readlines():
            if '<' in line:
                tags.add(line[line.index('<'):line.index('>') + 1])
        return tags


def parse_spells():
    with open('all_spells.txt', 'r') as f:
        lines = f.readlines()
        groups = []
        group = []
        for line in lines:
            if line == delimiter:
                groups.append(''.join(group))
                group = []
            else:
                group.append(line)
    return groups


def format_as_func_name(txt):
    r_list = [' ', '/', "'"]
    out = txt.lower()
    for char in r_list:
        out = out.replace(char, '_')
    if out == '5th-level_evocation_':
        out = 'cone_of_cold'
    return out


def format_spell_text(txt):
    out = txt
    newline_runs = []
    if '\n' in out:
        on_run = False
        for char in out:
            if on_run and char == '\n':
                newline_runs[-1] += 1
            elif char == '\n':
                newline_runs.append(1)
                on_run = True
            else:
                on_run = False
    
    newline_runs = list(set(newline_runs))
    newline_runs.sort(reverse=True)
    
    for i in newline_runs:
        if i == 1:
            break
        out = out.replace(''.join(['\n' for _ in range(i)]), '')
    out = out.replace('.', '.\n').replace('\n', '\n    ')
    out = out.rstrip()
    return out

    
def generate_spell_code(spell_html):
    soup = BeautifulSoup(spell_html, 'html.parser')
    text = soup.getText()
    spell_name = format_as_func_name(text.splitlines()[0])
    spell_text = format_spell_text(text)
    template = f"""@spell
def {spell_name}(upcast=None):
    '''
    {spell_text}
    '''
    print({spell_name}.__doc__)


"""
    return template


if __name__ =='__main__':
    spells = parse_spells()
    with open('gen_spells.py', 'w') as f:
        f.write('from man_spells import spell\n\n\n')
        for spell in spells:
            f.write(generate_spell_code(spell))

