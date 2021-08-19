
from bs4 import BeautifulSoup
# import lxml


def get_element(node):
    # for XPATH we have to count only for nodes with same type!
    length = len(list(node.previous_siblings)) + 1
    if (length) > 1:
        return '%s:nth-child(%s)' % (node.name, length)
    else:
        return node.name


def get_css_path(node):
    path = [get_element(node)]
    for parent in node.parents:
        if parent.name == 'body':
            break
        path.insert(0, get_element(parent))
    return ' > '.join(path)


soup = BeautifulSoup(
    '<div></div><div><strong><i>bla</i></strong></div>', "lxml")
# assert get_css_path(soup.i) == 'div:nth-child(2) > strong > i'
print(soup.i)
