import re

def _inline_replace(text: str) -> str:
    """Substituições inline: imagem, link, bold e itálico."""
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1"/>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    return text

def markdown_to_html(md: str) -> str:
    """Converte Markdown básico para HTML."""
    lines = md.splitlines()
    out, in_ol = [], False

    for line in lines:
        # Cabeçalhos
        if m := re.match(r'^\s*(#{1,3})\s+(.*)$', line):
            if in_ol:
                out.append('</ol>')
                in_ol = False
            level = len(m.group(1))
            out.append(f'<h{level}>{_inline_replace(m.group(2).strip())}</h{level}>')
            continue

        # Lista numerada
        if m := re.match(r'^\s*\d+\.\s+(.*)$', line):
            if not in_ol:
                out.append('<ol>')
                in_ol = True
            out.append(f'<li>{_inline_replace(m.group(1).strip())}</li>')
            continue
        elif in_ol:
            out.append('</ol>')
            in_ol = False

        # Texto normal
        out.append(_inline_replace(line) if line.strip() else '')

    if in_ol:
        out.append('</ol>')

    return '\n'.join(out)

# Exemplo de uso
if __name__ == "__main__":
    sample_md = """# Exemplo

Este é um **exemplo** com *itálico* e **negrito**.

Como pode ser consultado em [página da UC](http://www.uc.pt)

Como se vê na imagem seguinte: ![imagem dum coelho](http://www.coellho.com) ...

1. Primeiro item
2. Segundo item
3. Terceiro item
"""
    print(markdown_to_html(sample_md))
