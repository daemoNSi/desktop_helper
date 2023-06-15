# client id - 510313067182-brnkq8et1gj5v023j64fus90q2gftu8k.apps.googleusercontent.com
# Client secret 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
import webbrowser
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from win10toast import ToastNotifier
from easygui import enterbox

SCOPES = ['https://www.googleapis.com/auth/documents']
creds = Credentials.from_authorized_user_file('token.json', SCOPES)
doc_data = []


def lookup_word():
    word_search = enterbox('Word to search on Jisho:')
    if len(word_search) == 0:
        pass
    else:
        webbrowser.open_new_tab(f'https://jisho.org/search/{word_search}')


def upd_cont():
    doc_data.clear()
    service = build('docs', 'v1', credentials=creds)
    DOCUMENT_ID = '1mHqClLSgTHNHp108l1_spSCjHDUQPbv0gdOHfc2cZkQ'
    doc = service.documents().get(documentId=DOCUMENT_ID).execute()
    doc_content = doc.get('body').get('content')
    doc_data.append(service)
    doc_data.append(doc)
    doc_data.append(doc_content)
    doc_data.append(DOCUMENT_ID)


def jisho_search(word):
    webbrowser.open_new_tab(f'https://jisho.org/search/{word}')


def duplicate_check(insert_word):
    upd_cont()
    doc_list = read_data(doc_data[2])
    for i in doc_list:
        if i != '\n':
            if i == insert_word:
                return False
    return True


def insert_to_doc(word):
    upd_cont()
    if duplicate_check(word) is False:
        toast = ToastNotifier()
        toast.show_toast('Duplicate error', f'{word} is a duplicate', duration=2)
        return False
    else:
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': word + '\n'
                }
            },
        ]
        result = doc_data[0].documents().batchUpdate(documentId=doc_data[3], body={'requests': requests}).execute()


def get_data(element):
    text_run = element.get('textRun')
    if not text_run:
        return 'empty'
    return text_run.get('content')


def read_data(elements):
    text = ''
    list_text = []
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += get_data(elem)
                list_text.append(get_data(elem).strip('\n'))
        elif 'table' in value:
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_data(cell.get('content'))
        elif 'tableContents' in value:
            toc = value.get('tableContents')
            text += read_data(toc.get('content'))
    return list_text
