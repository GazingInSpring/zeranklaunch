from bs4 import BeautifulSoup
from pathlib import Path

def render_now(input_html, output_html):
    with open(input_html, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Remove Tailwind CDN (not needed, everything is inline styled)
    for script in soup.find_all('script', src=lambda x: x and 'tailwind' in x):
        script.decompose()
    
    # Inline all iframe HTML files
    for iframe in soup.find_all('iframe'):
        src = iframe.get('src', '')
        if not src or src.startswith('http'):
            continue
        
        try:
            with open(src, 'r', encoding='utf-8') as f:
                iframe_soup = BeautifulSoup(f.read(), 'html.parser')
            
            div = soup.new_tag('div')
            div['style'] = iframe.get('style', '')
            
            # Move iframe styles to head
            for style in iframe_soup.find_all('style'):
                soup.head.append(style)
            
            # Move iframe content to div
            if iframe_soup.body:
                for child in list(iframe_soup.body.children):
                    div.append(child)
            
            # Move iframe scripts to body
            for script in iframe_soup.find_all('script'):
                soup.body.append(script)
            
            iframe.replace_with(div)
            print(f"✓ {src}")
            
        except Exception as e:
            print(f"✗ {src}: {e}")
    
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
    
    print(f"\n✅ {output_html} ({Path(output_html).stat().st_size / 1024:.0f} KB)")

render_now('blog.html', 'rendered_blog.html')